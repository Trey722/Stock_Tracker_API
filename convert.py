import pandas as pd

def convert_pandas_json(data):
    try:
        return pd.DataFrame(data).to_json(orient='split', date_format='iso', index=False)
    except Exception as e:
        return f"Error converting to Pandas: {e}"
    
    
def convert_optoin_chain_to_json(data):
    call = pd.DataFrame(data[0]).to_json(orient='records')  # Convert to JSON
    put = pd.DataFrame(data[1]).to_json(orient='records')  # Convert to JSON
    
    return {"call": call, "put": put}