import sys
import logging
import argparse
import json
import gphoto2 as gp

def list_cameras(output_json=False):
    try:
        # Create library context
        context = gp.Context()
        
        # Detect connected cameras
        camera_list = gp.Camera.autodetect(context)
        
        cameras = []
        for index in range(len(camera_list)):
            name = camera_list.get_name(index)
            port = camera_list.get_value(index)
            cameras.append({
                "index": index,
                "name": name,
                "port": port
            })
            
        if output_json:
            print(json.dumps(cameras, indent=2))
        else:
            if not cameras:
                print("No cameras detected. Make sure the camera is powered on and connected via USB.")
            else:
                print(f"Found {len(cameras)} camera(s):")
                for cam in cameras:
                    print(f"  [{cam['index']}] Name: {cam['name']}")
                    print(f"      Port: {cam['port']}")
        
        return len(cameras)
    except gp.GPhoto2Error as e:
        logging.error(f"gphoto2 error: {e}")
        return -1
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        return -1

def main():
    parser = argparse.ArgumentParser(
        description="CLI utility to list available gphoto2 cameras."
    )
    parser.add_argument(
        "-j", "--json", 
        action="store_true", 
        help="Output detected cameras in JSON format"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable verbose debug logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    
    count = list_cameras(output_json=args.json)
    if count < 0:
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
