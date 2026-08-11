import os, uuid

def get_device_id():
    """Get or create a persistent UUID for this device."""
    # Store in app private directory
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    id_file = os.path.join(base, 'device_id.txt')
    
    if os.path.exists(id_file):
        try:
            with open(id_file, 'r') as f:
                return f.read().strip()
        except:
            pass
    
    dev_id = str(uuid.uuid4())
    try:
        with open(id_file, 'w') as f:
            f.write(dev_id)
    except:
        pass
    return dev_id
