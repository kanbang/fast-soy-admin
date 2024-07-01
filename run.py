'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2024-05-31 21:27:14
LastEditors: zhai
LastEditTime: 2024-06-29 08:53:55
'''
import uvicorn

from app.log.log import LOGGING_CONFIG

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9999, reload=False, log_config=LOGGING_CONFIG)
