from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from config import Config
from contract_handler.web3 import ContractHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Initialize Web3 contract handler
    contract_handler = ContractHandler()
    
    @app.route('/', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'Flask Web3 server is running',
            'network': contract_handler.get_network_info()
        })
    
    @app.route('/api/balance/<address>', methods=['GET'])
    def get_balance(address):
        """Get ETH balance for an address"""
        try:
            balance = contract_handler.get_balance(address)
            return jsonify({
                'success': True,
                'address': address,
                'balance': balance,
                'unit': 'ETH'
            })
        except Exception as e:
            logger.error(f"Error getting balance: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @app.route('/api/contract/call', methods=['POST'])
    def call_contract():
        """Call a read-only contract function"""
        try:
            data = request.get_json()
            contract_address = data.get('contract_address')
            function_name = data.get('function_name')
            function_args = data.get('function_args', [])
            
            if not contract_address or not function_name:
                return jsonify({
                    'success': False,
                    'error': 'contract_address and function_name are required'
                }), 400
            
            result = contract_handler.call_contract_function(
                contract_address, 
                function_name, 
                function_args
            )
            
            return jsonify({
                'success': True,
                'result': result,
                'contract_address': contract_address,
                'function_name': function_name
            })
            
        except Exception as e:
            logger.error(f"Error calling contract: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @app.route('/api/contract/transaction', methods=['POST'])
    def send_transaction():
        """Send a transaction to a contract"""
        try:
            data = request.get_json()
            contract_address = data.get('contract_address')
            function_name = data.get('function_name')
            function_args = data.get('function_args', [])
            value = data.get('value', 0)  # ETH value to send
            
            if not contract_address or not function_name:
                return jsonify({
                    'success': False,
                    'error': 'contract_address and function_name are required'
                }), 400
            
            tx_hash = contract_handler.send_transaction(
                contract_address,
                function_name,
                function_args,
                value
            )
            
            return jsonify({
                'success': True,
                'transaction_hash': tx_hash,
                'contract_address': contract_address,
                'function_name': function_name
            })
            
        except Exception as e:
            logger.error(f"Error sending transaction: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @app.route('/api/transaction/<tx_hash>', methods=['GET'])
    def get_transaction(tx_hash):
        """Get transaction details"""
        try:
            tx_details = contract_handler.get_transaction_details(tx_hash)
            return jsonify({
                'success': True,
                'transaction': tx_details
            })
        except Exception as e:
            logger.error(f"Error getting transaction: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @app.route('/api/contract/events', methods=['POST'])
    def get_contract_events():
        """Get contract events"""
        try:
            data = request.get_json()
            contract_address = data.get('contract_address')
            event_name = data.get('event_name')
            from_block = data.get('from_block', 'latest')
            to_block = data.get('to_block', 'latest')
            
            if not contract_address or not event_name:
                return jsonify({
                    'success': False,
                    'error': 'contract_address and event_name are required'
                }), 400
            
            events = contract_handler.get_contract_events(
                contract_address,
                event_name,
                from_block,
                to_block
            )
            
            return jsonify({
                'success': True,
                'events': events,
                'count': len(events)
            })
            
        except Exception as e:
            logger.error(f"Error getting events: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )
