import jwt
from datetime import timedelta, datetime
from typing import Any, Callable, Dict
from configs.config import JWT_KEY

def verify_token(token: str) -> bool:
    
    try:
        data: Dict[str, Any] = jwt.decode(token, JWT_KEY, 'HS256')
        expires = data.get('expires', (datetime.now() + timedelta(days=1)).timestamp())
        expires = datetime.fromtimestamp(expires)
        
        if expires < datetime.now():
            return False
        else:
            return True
    except:
        return False