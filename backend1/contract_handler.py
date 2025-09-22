import json
import os
from typing import Dict, List, Any, Optional
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
import logging
from config import Config

logger = logging.getLogger(__name__)

class ContractHandler:
    """Web3 contract interaction handler"""
    
    def __init__(self):
        """Initialize Web3 connection and account"""
        self.config = Config()
        self.w3 = self._initialize_web3()
        self.account = self._load_account() if self.config.PRIVATE_KEY else None
        self._contract_cache = {}
        self._abi_cache = {}
    
    def _initialize_web3(self) -> Web3:
        """Initialize Web3 connection"""
        try:
            provider_url = self.config.get_web3_provider_url()
            
            if provider_url.startswith('http'):
                w3 = Web3(Web3.HTTPProvider(provider_url))
            elif provider_url.startswith('ws'):
                w3 = Web3(Web3.WebsocketProvider(provider_url))
            else:
                raise ValueError(f"Unsupported provider URL: {provider_url}")
            
            # Add PoA middleware if on a testnet (required for some testnets)
            if self.config.is_testnet():
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            # Test connection
            if not w3.is_connected():
                raise ConnectionError("Failed to connect to Web3 provider")
            
            logger.info(f"Connected to Web3 provider: {provider_url}")
            logger.info(f"Latest block: {w3.eth.block_number}")
            
            return w3
            
        except Exception as e:
            logger.error(f"Failed to initialize Web3: {str(e)}")
            raise
    
    def _load_account(self) -> Account:
        """Load account from private key"""
        try:
            if not self.config.PRIVATE_KEY:
                return None
            
            account = Account.from_key(self.config.PRIVATE_KEY)
            
            if self.config.WALLET_ADDRESS:
                if account.address.lower() != self.config.WALLET_ADDRESS.lower():
                    raise ValueError("Private key does not match wallet address")
            
            logger.info(f"Loaded account: {account.address}")
            return account
            
        except Exception as e:
            logger.error(f"Failed to load account: {str(e)}")
            raise
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        try:
            return {
                'network_id': self.w3.eth.chain_id,
                'network_name': self.config.NETWORK_NAME,
                'latest_block': self.w3.eth.block_number,
                'gas_price': str(self.w3.eth.gas_price),
                'is_testnet': self.config.is_testnet(),
                'connected': self.w3.is_connected()
            }
        except Exception as e:
            logger.error(f"Error getting network info: {str(e)}")
            return {'error': str(e)}
    
    def get_balance(self, address: str) -> float:
        """Get ETH balance for an address"""
        try:
            if not Web3.is_address(address):
                raise ValueError(f"Invalid address: {address}")
            
            balance_wei = self.w3.eth.get_balance(Web3.to_checksum_address(address))
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            return float(balance_eth)
            
        except Exception as e:
            logger.error(f"Error getting balance for {address}: {str(e)}")
            raise
    
    def load_contract_abi(self, abi_path: str) -> List[Dict]:
        """Load contract ABI from file"""
        try:
            if abi_path in self._abi_cache:
                return self._abi_cache[abi_path]
            
            if not os.path.exists(abi_path):
                # Try with default ABI path
                full_path = os.path.join(self.config.DEFAULT_CONTRACT_ABI_PATH, abi_path)
                if not os.path.exists(full_path):
                    raise FileNotFoundError(f"ABI file not found: {abi_path}")
                abi_path = full_path
            
            with open(abi_path, 'r') as f:
                abi = json.load(f)
            
            self._abi_cache[abi_path] = abi
            return abi
            
        except Exception as e:
            logger.error(f"Error loading ABI from {abi_path}: {str(e)}")
            raise
    
    def get_contract(self, contract_address: str, abi_path: str = None, abi: List[Dict] = None):
        """Get contract instance"""
        try:
            if not Web3.is_address(contract_address):
                raise ValueError(f"Invalid contract address: {contract_address}")
            
            checksum_address = Web3.to_checksum_address(contract_address)
            cache_key = f"{checksum_address}_{abi_path or 'custom'}"
            
            if cache_key in self._contract_cache:
                return self._contract_cache[cache_key]
            
            if abi is None:
                if abi_path is None:
                    raise ValueError("Either abi_path or abi must be provided")
                abi = self.load_contract_abi(abi_path)
            
            contract = self.w3.eth.contract(address=checksum_address, abi=abi)
            self._contract_cache[cache_key] = contract
            
            return contract
            
        except Exception as e:
            logger.error(f"Error getting contract {contract_address}: {str(e)}")
            raise
    
    def call_contract_function(self, contract_address: str, function_name: str, 
                             function_args: List = None, abi_path: str = None, 
                             abi: List[Dict] = None) -> Any:
        """Call a read-only contract function"""
        try:
            contract = self.get_contract(contract_address, abi_path, abi)
            function_args = function_args or []
            
            # Get the contract function
            contract_function = getattr(contract.functions, function_name)
            
            # Call the function
            result = contract_function(*function_args).call()
            
            # Convert Web3 data types to serializable formats
            if isinstance(result, bytes):
                result = result.hex()
            elif hasattr(result, '_asdict'):  # Named tuple
                result = result._asdict()
            
            logger.info(f"Called {function_name} on {contract_address}: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error calling {function_name} on {contract_address}: {str(e)}")
            raise
    
    def send_transaction(self, contract_address: str, function_name: str,
                        function_args: List = None, value: int = 0,
                        abi_path: str = None, abi: List[Dict] = None) -> str:
        """Send a transaction to a contract function"""
        try:
            if not self.account:
                raise ValueError("No account loaded for sending transactions")
            
            contract = self.get_contract(contract_address, abi_path, abi)
            function_args = function_args or []
            
            # Get the contract function
            contract_function = getattr(contract.functions, function_name)
            
            # Build transaction
            transaction = contract_function(*function_args).build_transaction({
                'from': self.account.address,
                'gas': self.config.GAS_LIMIT,
                'gasPrice': self.config.get_gas_price_wei(),
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'value': value
            })
            
            # Sign transaction
            signed_txn = self.account.sign_transaction(transaction)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_hash_hex = tx_hash.hex()
            
            logger.info(f"Sent transaction {tx_hash_hex} to {function_name} on {contract_address}")
            return tx_hash_hex
            
        except Exception as e:
            logger.error(f"Error sending transaction to {function_name} on {contract_address}: {str(e)}")
            raise
    
    def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction details and receipt"""
        try:
            # Get transaction
            tx = self.w3.eth.get_transaction(tx_hash)
            
            # Try to get receipt (may not exist if not mined yet)
            try:
                receipt = self.w3.eth.get_transaction_receipt(tx_hash)
                receipt_data = {
                    'block_number': receipt.blockNumber,
                    'gas_used': receipt.gasUsed,
                    'status': receipt.status,
                    'logs': [dict(log) for log in receipt.logs]
                }
            except:
                receipt_data = None
            
            return {
                'hash': tx_hash,
                'from': tx['from'],
                'to': tx['to'],
                'value': str(tx['value']),
                'gas': tx['gas'],
                'gas_price': str(tx['gasPrice']),
                'nonce': tx['nonce'],
                'block_number': tx.get('blockNumber'),
                'transaction_index': tx.get('transactionIndex'),
                'receipt': receipt_data
            }
            
        except Exception as e:
            logger.error(f"Error getting transaction details for {tx_hash}: {str(e)}")
            raise
    
    def get_contract_events(self, contract_address: str, event_name: str,
                          from_block: str = 'latest', to_block: str = 'latest',
                          abi_path: str = None, abi: List[Dict] = None) -> List[Dict]:
        """Get contract events"""
        try:
            contract = self.get_contract(contract_address, abi_path, abi)
            
            # Get the event
            event_filter = getattr(contract.events, event_name)
            
            # Get events
            events = event_filter.get_logs(fromBlock=from_block, toBlock=to_block)
            
            # Convert to serializable format
            result = []
            for event in events:
                event_data = {
                    'event': event_name,
                    'transaction_hash': event['transactionHash'].hex(),
                    'block_number': event['blockNumber'],
                    'args': dict(event['args']),
                    'address': event['address'],
                    'log_index': event['logIndex']
                }
                result.append(event_data)
            
            logger.info(f"Retrieved {len(result)} {event_name} events from {contract_address}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting {event_name} events from {contract_address}: {str(e)}")
            raise
    
    def wait_for_transaction_receipt(self, tx_hash: str, timeout: int = 120) -> Dict:
        """Wait for transaction to be mined"""
        try:
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
            return dict(receipt)
        except Exception as e:
            logger.error(f"Error waiting for transaction receipt {tx_hash}: {str(e)}")
            raise
    
    def estimate_gas(self, contract_address: str, function_name: str,
                    function_args: List = None, value: int = 0,
                    abi_path: str = None, abi: List[Dict] = None) -> int:
        """Estimate gas for a transaction"""
        try:
            if not self.account:
                raise ValueError("No account loaded for gas estimation")
            
            contract = self.get_contract(contract_address, abi_path, abi)
            function_args = function_args or []
            
            # Get the contract function
            contract_function = getattr(contract.functions, function_name)
            
            # Estimate gas
            gas_estimate = contract_function(*function_args).estimate_gas({
                'from': self.account.address,
                'value': value
            })
            
            logger.info(f"Gas estimate for {function_name}: {gas_estimate}")
            return gas_estimate
            
        except Exception as e:
            logger.error(f"Error estimating gas for {function_name}: {str(e)}")
            raise
