## Moodle Python Client (Basic)

A minimal Python client to call Moodle's REST web services and a small example to fetch site info.

### Prerequisites
- Python 3.8+
- A Moodle web service token with the functions you need enabled. For a quick test, ensure `core_webservice_get_site_info` is allowed.

How to create a token in Moodle:
- Site administration → Server → Web services → Manage tokens
- Create a token tied to a service that includes the required functions

### Install

```bash
python -m pip install -r requirements.txt
```

### Configure

You can pass settings via CLI flags or environment variables. Using a `.env` file is convenient during development.

Create `.env` (or copy `.env.example`):

```env
MOODLE_BASE_URL=https://your-moodle.example.com
MOODLE_TOKEN=your_moodle_token_here
```

### Run the example

- Using env vars (from `.env`):

```bash
python example.py
```

- Or explicitly via CLI:

```bash
python example.py --base-url https://your-moodle.example.com --token your_moodle_token_here
```

Expected output is JSON describing your Moodle site, for example:

```json
{
  "downloadfiles": 1,
  "firstname": "Admin",
  "fullname": "Site Full Name",
  "username": "admin",
  "usercanmanageownfiles": 1
}
```

### Using the client in your code

```python
from moodle_client import MoodleClient

client = MoodleClient(base_url="https://your-moodle.example.com", token="your_token")
site_info = client.get_site_info()
users = client.get_users_by_field(field="email", values=["teacher@example.com"])  # returns a list
```

### Notes
- Most functions and parameter shapes are documented in your Moodle instance under: `/admin/webservice/documentation.php`.
- When passing lists/dicts to `client.call(...)`, parameters are automatically encoded into Moodle's expected bracket notation (e.g., `param[0][sub]`).
- Errors from Moodle are raised as `MoodleError`.