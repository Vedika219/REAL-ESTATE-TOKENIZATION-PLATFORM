<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Contract Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e1e5e9;
        }

        h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            font-weight: 700;
        }

        h2 {
            color: #34495e;
            margin-bottom: 20px;
            font-size: 1.5rem;
        }

        .wallet-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .wallet-info {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            font-size: 0.9rem;
            color: #555;
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn-primary {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
        }

        .btn-primary:hover {
            background: linear-gradient(45deg, #2980b9, #1f6391);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }

        .btn-secondary {
            background: linear-gradient(45deg, #95a5a6, #7f8c8d);
            color: white;
        }

        .btn-secondary:hover {
            background: linear-gradient(45deg, #7f8c8d, #6c7b7d);
            transform: translateY(-2px);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .status-section {
            margin-bottom: 30px;
            text-align: center;
        }

        .status-message {
            padding: 15px;
            border-radius: 8px;
            font-weight: 500;
            margin-bottom: 10px;
        }

        .status-message.success {
            background: #d5f4e6;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .status-message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .status-message.info {
            background: #cce7ff;
            color: #004085;
            border: 1px solid #b3d7ff;
        }

        .network-info {
            font-size: 0.9rem;
            color: #666;
        }

        .contract-section {
            display: grid;
            gap: 30px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            border: 1px solid #e1e5e9;
        }

        .info-grid {
            display: grid;
            gap: 15px;
        }

        .info-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .info-item label {
            font-weight: 600;
            color: #555;
        }

        .input-field {
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
            width: 100%;
            margin-bottom: 10px;
        }

        .input-field:focus {
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }

        .function-group {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 20px;
        }

        .input-group {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
        }

        .input-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }

        .results-section {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            min-height: 50px;
            border-left: 4px solid #3498db;
        }

        .transaction-list {
            max-height: 300px;
            overflow-y: auto;
        }

        .transaction-item {
            padding: 15px;
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            margin-bottom: 10px;
            background: #f8f9fa;
        }

        .transaction-hash {
            font-family: monospace;
            font-size: 0.9rem;
            color: #666;
            word-break: break-all;
        }

        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }

        .loading-overlay p {
            color: white;
            font-size: 18px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .hidden {
            display: none !important;
        }

        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }

            header {
                flex-direction: column;
                gap: 20px;
            }

            h1 {
                font-size: 2rem;
            }

            .function-group {
                flex-direction: column;
            }

            .btn {
                width: 100%;
            }
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ethers/6.7.1/ethers.umd.min.js"></script>
</head>
<body>
    <div class="container">
        <header>
            <h1>Smart Contract Interface</h1>
            <div class="wallet-section">
                <button id="connectWallet" class="btn btn-primary">Connect Wallet</button>
                <div id="walletInfo" class="wallet-info hidden">
                    <span id="walletAddress"></span>
                    <span id="walletBalance"></span>
                </div>
            </div>
        </header>

        <main>
            <div class="status-section">
                <div id="status" class="status-message">Please connect your wallet to continue</div>
                <div id="networkInfo" class="network-info hidden">
                    <span>Network: <span id="currentNetwork"></span></span>
                </div>
            </div>

            <div class="contract-section">
                <div class="card">
                    <h2>Contract Information</h2>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>Contract Address:</label>
                            <input type="text" id="contractAddress" placeholder="Enter contract address" class="input-field">
                        </div>
                        <div class="info-item">
                            <label>Contract Balance:</label>
                            <span id="contractBalance">-</span>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h2>Read Functions</h2>
                    <div class="function-group">
                        <button id="getName" class="btn btn-secondary">Get Name</button>
                        <button id="getSymbol" class="btn btn-secondary">Get Symbol</button>
                        <button id="getTotalSupply" class="btn btn-secondary">Get Total Supply</button>
                        <button id="getBalance" class="btn btn-secondary">Get My Balance</button>
                    </div>
                    <div id="readResults" class="results-section"></div>
                </div>

                <div class="card">
                    <h2>Write Functions</h2>
                    <div class="function-group">
                        <div class="input-group">
                            <label for="transferTo">Transfer To:</label>
                            <input type="text" id="transferTo" placeholder="Recipient address" class="input-field">
                            <label for="transferAmount">Amount:</label>
                            <input type="number" id="transferAmount" placeholder="Amount" class="input-field">
                            <button id="transfer" class="btn btn-primary">Transfer</button>
                        </div>
                        
                        <div class="input-group">
                            <label for="mintTo">Mint To:</label>
                            <input type="text" id="mintTo" placeholder="Recipient address" class="input-field">
                            <label for="mintAmount">Amount:</label>
                            <input type="number" id="mintAmount" placeholder="Amount" class="input-field">
                            <button id="mint" class="btn btn-primary">Mint</button>
                        </div>
                        
                        <div class="input-group">
                            <label for="approveSpender">Approve Spender:</label>
                            <input type="text" id="approveSpender" placeholder="Spender address" class="input-field">
                            <label for="approveAmount">Amount:</label>
                            <input type="number" id="approveAmount" placeholder="Amount" class="input-field">
                            <button id="approve" class="btn btn-primary">Approve</button>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h2>Transaction History</h2>
                    <div id="transactionHistory" class="transaction-list"></div>
                </div>
            </div>
        </main>

        <div id="loadingOverlay" class="loading-overlay hidden">
            <div class="loading-spinner"></div>
            <p>Processing transaction...</p>
        </div>
    </div>

    <script>
        // Global variables
        let provider;
        let signer;
        let contract;
        let userAccount;

        // Contract configuration - Update these with your contract details
        const CONTRACT_CONFIG = {
            address: '', // Add your contract address here
            abi: [
                // Standard ERC20 ABI functions - Replace with your contract ABI
                "function name() view returns (string)",
                "function symbol() view returns (string)",
                "function totalSupply() view returns (uint256)",
                "function balanceOf(address) view returns (uint256)",
                "function transfer(address to, uint256 amount) returns (bool)",
                "function approve(address spender, uint256 amount) returns (bool)",
                "function mint(address to, uint256 amount) returns (bool)",
                "event Transfer(address indexed from, address indexed to, uint256 value)"
            ]
        };

        // DOM elements
        const elements = {
            connectWallet: document.getElementById('connectWallet'),
            walletInfo: document.getElementById('walletInfo'),
            walletAddress: document.getElementById('walletAddress'),
            walletBalance: document.getElementById('walletBalance'),
            status: document.getElementById('status'),
            networkInfo: document.getElementById('networkInfo'),
            currentNetwork: document.getElementById('currentNetwork'),
            contractAddress: document.getElementById('contractAddress'),
            contractBalance: document.getElementById('contractBalance'),
            readResults: document.getElementById('readResults'),
            transactionHistory: document.getElementById('transactionHistory'),
            loadingOverlay: document.getElementById('loadingOverlay')
        };

        // Initialize the application
        window.addEventListener('DOMContentLoaded', async () => {
            setupEventListeners();
            checkWalletConnection();
        });

        // Setup event listeners
        function setupEventListeners() {
            elements.connectWallet.addEventListener('click', connectWallet);
            
            // Read function buttons
            document.getElementById('getName').addEventListener('click', () => callReadFunction('name'));
            document.getElementById('getSymbol').addEventListener('click', () => callReadFunction('symbol'));
            document.getElementById('getTotalSupply').addEventListener('click', () => callReadFunction('totalSupply'));
            document.getElementById('getBalance').addEventListener('click', () => callReadFunction('balanceOf', [userAccount]));
            
            // Write function buttons
            document.getElementById('transfer').addEventListener('click', handleTransfer);
            document.getElementById('mint').addEventListener('click', handleMint);
            document.getElementById('approve').addEventListener('click', handleApprove);
            
            // Contract address input
            elements.contractAddress.addEventListener('change', updateContractAddress);
        }

        // Check if wallet is already connected
        async function checkWalletConnection() {
            if (typeof window.ethereum !== 'undefined') {
                try {
                    const accounts = await window.ethereum.request({ method: 'eth_accounts' });
                    if (accounts.length > 0) {
                        await initializeProvider();
                        await updateWalletInfo();
                    }
                } catch (error) {
                    console.error('Error checking wallet connection:', error);
                }
            }
        }

        // Connect wallet
        async function connectWallet() {
            if (typeof window.ethereum === 'undefined') {
                showStatus('Please install MetaMask or another Web3 wallet', 'error');
                return;
            }

            try {
                showLoading(true);
                await window.ethereum.request({ method: 'eth_requestAccounts' });
                await initializeProvider();
                await updateWalletInfo();
                showStatus('Wallet connected successfully!', 'success');
            } catch (error) {
                console.error('Error connecting wallet:', error);
                showStatus('Failed to connect wallet: ' + error.message, 'error');
            } finally {
                showLoading(false);
            }
        }

        // Initialize provider and signer
        async function initializeProvider() {
            provider = new ethers.BrowserProvider(window.ethereum);
            signer = await provider.getSigner();
            userAccount = await signer.getAddress();

            // Listen for account changes
            window.ethereum.on('accountsChanged', handleAccountsChanged);
            window.ethereum.on('chainChanged', handleChainChanged);
        }

        // Update wallet information
        async function updateWalletInfo() {
            if (!signer) return;

            try {
                const address = await signer.getAddress();
                const balance = await provider.getBalance(address);
                const network = await provider.getNetwork();

                elements.walletAddress.textContent = `${address.slice(0, 6)}...${address.slice(-4)}`;
                elements.walletBalance.textContent = `${ethers.formatEther(balance)} ETH`;
                elements.currentNetwork.textContent = network.name;

                elements.connectWallet.style.display = 'none';
                elements.walletInfo.classList.remove('hidden');
                elements.networkInfo.classList.remove('hidden');

                // Initialize contract if address is set
                if (elements.contractAddress.value) {
                    initializeContract();
                }
            } catch (error) {
                console.error('Error updating wallet info:', error);
                showStatus('Error updating wallet information', 'error');
            }
        }

        // Initialize contract
        function initializeContract() {
            try {
                const address = elements.contractAddress.value;
                if (!address || !ethers.isAddress(address)) {
                    showStatus('Please enter a valid contract address', 'error');
                    return;
                }

                contract = new ethers.Contract(address, CONTRACT_CONFIG.abi, signer);
                updateContractInfo();
                showStatus('Contract initialized successfully!', 'success');
            } catch (error) {
                console.error('Error initializing contract:', error);
                showStatus('Error initializing contract: ' + error.message, 'error');
            }
        }

        // Update contract address
        function updateContractAddress() {
            if (signer && elements.contractAddress.value) {
                initializeContract();
            }
        }

        // Update contract information
        async function updateContractInfo() {
            if (!contract) return;

            try {
                const balance = await provider.getBalance(contract.target);
                elements.contractBalance.textContent = `${ethers.formatEther(balance)} ETH`;
            } catch (error) {
                console.error('Error updating contract info:', error);
            }
        }

        // Call read functions
        async function callReadFunction(functionName, params = []) {
            if (!contract) {
                showStatus('Please set a valid contract address first', 'error');
                return;
            }

            try {
                showLoading(true);
                const result = await contract[functionName](...params);
                displayResult(functionName, result);
            } catch (error) {
                console.error(`Error calling ${functionName}:`, error);
                showStatus(`Error calling ${functionName}: ${error.message}`, 'error');
            } finally {
                showLoading(false);
            }
        }

        // Handle transfer function
        async function handleTransfer() {
            const to = document.getElementById('transferTo').value;
            const amount = document.getElementById('transferAmount').value;

            if (!to || !amount) {
                showStatus('Please fill in all transfer fields', 'error');
                return;
            }

            try {
                const parsedAmount = ethers.parseEther(amount);
                await executeTransaction('transfer', [to, parsedAmount]);
            } catch (error) {
                showStatus('Error in transfer: ' + error.message, 'error');
            }
        }

        // Handle mint function
        async function handleMint() {
            const to = document.getElementById('mintTo').value;
            const amount = document.getElementById('mintAmount').value;

            if (!to || !amount) {
                showStatus('Please fill in all mint fields', 'error');
                return;
            }

            try {
                const parsedAmount = ethers.parseEther(amount);
                await executeTransaction('mint', [to, parsedAmount]);
            } catch (error) {
                showStatus('Error in mint: ' + error.message, 'error');
            }
        }

        // Handle approve function
        async function handleApprove() {
            const spender = document.getElementById('approveSpender').value;
            const amount = document.getElementById('approveAmount').value;

            if (!spender || !amount) {
                showStatus('Please fill in all approve fields', 'error');
                return;
            }

            try {
                const parsedAmount = ethers.parseEther(amount);
                await executeTransaction('approve', [spender, parsedAmount]);
            } catch (error) {
                showStatus('Error in approve: ' + error.message, 'error');
            }
        }

        // Execute transaction
        async function executeTransaction(functionName, params) {
            if (!contract) {
                showStatus('Please set a valid contract address first', 'error');
                return;
            }

            try {
                showLoading(true);
                const tx = await contract[functionName](...params);
                showStatus(`Transaction sent: ${tx.hash}`, 'info');
                addTransactionToHistory(tx.hash, functionName, 'pending');

                const receipt = await tx.wait();
                showStatus(`Transaction confirmed: ${tx.hash}`, 'success');
                updateTransactionStatus(tx.hash, 'confirmed');
                
                // Update balances after successful transaction
                updateWalletInfo();
                updateContractInfo();
            } catch (error) {
                console.error(`Error executing ${functionName}:`, error);
                showStatus(`Transaction failed: ${error.message}`, 'error');
                updateTransactionStatus(tx?.hash, 'failed');
            } finally {
                showLoading(false);
            }
        }

        // Display read function results
        function displayResult(functionName, result) {
            const resultDiv = elements.readResults;
            const resultItem = document.createElement('div');
            resultItem.innerHTML = `
                <strong>${functionName}:</strong> 
                <span>${typeof result === 'bigint' ? result.toString() : result}</span>
            `;
            resultDiv.appendChild(resultItem);
        }

        // Add transaction to history
        function addTransactionToHistory(hash, type, status) {
            const historyDiv = elements.transactionHistory;
            const transactionItem = document.createElement('div');
            transactionItem.className = 'transaction-item';
            transactionItem.id = `tx-${hash}`;
            transactionItem.innerHTML = `
                <div><strong>Type:</strong> ${type}</div>
                <div><strong>Status:</strong> <span class="tx-status">${status}</span></div>
                <div><strong>Hash:</strong> <span class="transaction-hash">${hash}</span></div>
                <div><strong>Time:</strong> ${new Date().toLocaleString()}</div>
            `;
            historyDiv.insertBefore(transactionItem, historyDiv.firstChild);
        }

        // Update transaction status
        function updateTransactionStatus(hash, status) {
            if (!hash) return;
            const txElement = document.getElementById(`tx-${hash}`);
            if (txElement) {
                const statusElement = txElement.querySelector('.tx-status');
                if (statusElement) {
                    statusElement.textContent = status;
                    statusElement.className = `tx-status ${status}`;
                }
            }
        }

        // Show status message
        function showStatus(message, type = 'info') {
            elements.status.textContent = message;
            elements.status.className = `status-message ${type}`;
        }

        // Show/hide loading overlay
        function showLoading(show) {
            if (show) {
                elements.loadingOverlay.classList.remove('hidden');
            } else {
                elements.loadingOverlay.classList.add('hidden');
            }
        }

        // Handle account changes
        function handleAccountsChanged(accounts) {
            if (accounts.length === 0) {
                // User disconnected wallet
                resetWalletState();
            } else {
                // User switched accounts
                updateWalletInfo();
            }
        }

        // Handle chain changes
        function handleChainChanged(chainId) {
            // Reload the page to reinitialize with new chain
            window.location.reload();
        }

        // Reset wallet state
        function resetWalletState() {
            provider = null;
            signer = null;
            contract = null;
            userAccount = null;

            elements.connectWallet.style.display = 'block';
            elements.walletInfo.classList.add('hidden');
            elements.networkInfo.classList.add('hidden');
            
            showStatus('Please connect your wallet to continue', 'info');
        }
    </script>
</body>
</html>
