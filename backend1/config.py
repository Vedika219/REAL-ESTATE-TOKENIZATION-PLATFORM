import os
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Flask Web3 application"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # Web3 Configuration
    WEB3_PROVIDER_URL = os.environ.get('WEB3_PROVIDER_URL', 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID')
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY')  # Private key for transactions
    WALLET_ADDRESS = os.environ.get('WALLET_ADDRESS')  # Address corresponding to private key
    
    # Network Configuration
    NETWORK_ID = int(os.environ.get('NETWORK_ID', 1))  # 1 for mainnet, 11155111 for sepolia
    NETWORK_NAME = os.environ.get('NETWORK_NAME', 'mainnet')
    
    # Gas Configuration
    GAS_PRICE_GWEI = int(os.environ.get('GAS_PRICE_GWEI', 20))
    GAS_LIMIT = int(os.environ.get('GAS_LIMIT', 300000))
    
    # Contract Configuration
    DEFAULT_CONTRACT_ABI_PATH = os.environ.get('DEFAULT_CONTRACT_ABI_PATH', 'contracts/abi/')
    
    # API Configuration
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '100/hour')
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    
    # Database Configuration (if needed for caching, etc.)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
    
    # External API Keys
    ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')
    ALCHEMY_API_KEY = os.environ.get('ALCHEMY_API_KEY')
    INFURA_PROJECT_ID = os.environ.get('INFURA_PROJECT_ID')
    
    # Security Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    @classmethod
    def validate_config(cls):
        """Validate critical configuration values"""
        errors = []
        
        if not cls.WEB3_PROVIDER_URL or 'YOUR_PROJECT_ID' in cls.WEB3_PROVIDER_URL:
            errors.append("WEB3_PROVIDER_URL must be set with a valid provider URL")
        
        if cls.PRIVATE_KEY and not cls.PRIVATE_KEY.startswith('0x'):
            errors.append("PRIVATE_KEY must start with '0x'")
        
        if cls.WALLET_ADDRESS and not Web3.is_address(cls.WALLET_ADDRESS):
            errors.append("WALLET_ADDRESS must be a valid Ethereum address")
        
        if cls.PRIVATE_KEY and not cls.WALLET_ADDRESS:
            errors.append("WALLET_ADDRESS must be set when PRIVATE_KEY is provided")
        
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(f"- {error}" for error in errors))
        
        return True
    
    @classmethod
    def get_web3_provider_url(cls):
        """Get the appropriate Web3 provider URL based on configuration"""
        provider_url = cls.WEB3_PROVIDER_URL
        
        # Replace placeholders with actual API keys
        if cls.INFURA_PROJECT_ID and 'infura.io' in provider_url:
            provider_url = provider_url.replace('YOUR_PROJECT_ID', cls.INFURA_PROJECT_ID)
        elif cls.ALCHEMY_API_KEY and 'alchemyapi.io' in provider_url:
            provider_url = provider_url.replace('YOUR_API_KEY', cls.ALCHEMY_API_KEY)
        
        return provider_url
    
    @classmethod
    def get_gas_price_wei(cls):
        """Convert gas price from Gwei to Wei"""
        return Web3.to_wei(cls.GAS_PRICE_GWEI, 'gwei')
    
    @classmethod
    def is_testnet(cls):
        """Check if we're running on a testnet"""
        testnet_ids = [3, 4, 5, 42, 11155111]  # Ropsten, Rinkeby, Goerli, Kovan, Sepolia
        return cls.NETWORK_ID in testnet_ids

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    # Additional production-specific settings
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
    
    @classmethod
    def validate_config(cls):
        """Additional validation for production"""
        super().validate_config()
        
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set to a secure value in production")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    # Use a test network or local blockchain
    WEB3_PROVIDER_URL = 'http://localhost:8545'  # Local Ganache
    NETWORK_ID = 1337

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])
