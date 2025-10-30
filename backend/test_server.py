import sys
from pathlib import Path

# Ensure backend/ directory is on sys.path when running from backend/
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
	sys.path.insert(0, str(BACKEND_DIR))

# Validate core and registry imports
try:
	from core.entity import Entity  # noqa: F401
	print("[test_server] core.entity import OK")
except Exception as e:
	print(f"[test_server] core.entity import FAILED: {e}")

try:
	from transforms.registry import transform_registry  # noqa: F401
	print("[test_server] transforms.registry import OK")
except Exception as e:
	print(f"[test_server] transforms.registry import FAILED: {e}")

# Validate API imports
try:
	from api.main import app  # noqa: F401
	print("[test_server] api.main import OK")
except Exception as e:
	print(f"[test_server] api.main import FAILED: {e}")

if __name__ == "__main__":
	# Optional: run uvicorn if available
	try:
		import uvicorn
		uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=False)
	except Exception as e:
		print(f"[test_server] uvicorn run failed or not installed: {e}")
