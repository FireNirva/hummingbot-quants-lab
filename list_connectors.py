import asyncio  
from core.data_sources.clob import CLOBDataSource  
  
async def list_connectors():  
    # Initialize CLOBDataSource within an async function  
    clob = CLOBDataSource()  
      
    # Get all supported connectors  
    supported_connectors = list(clob.connectors.keys())  
    print("Supported connectors:", supported_connectors)  
      
    # Clean up any resources  
    for connector in clob.connectors.values():  
        if hasattr(connector, 'close'):  
            await connector.close()  
  
# Run the async function with asyncio.run()  
if __name__ == "__main__":  
    asyncio.run(list_connectors())