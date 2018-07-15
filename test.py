import sys
import json
def main(arg, arg2):
    data = json.dumps({"arg1": float(arg), "arg2": int(arg2)})
    print(data)
    sys.stdout.flush()
    
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])