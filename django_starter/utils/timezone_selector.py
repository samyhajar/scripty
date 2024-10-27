import sys
import subprocess
from pathlib import Path

try:
    from pick import pick
except ImportError:
    print("Installing required package: pick...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pick"])
    try:
        from pick import pick
    except ImportError:
        print("Failed to install pick. Please install it manually.")
        sys.exit(1)

class TimezoneSelector:
    def __init__(self):
        self.regions = {
            'Africa': [tz for tz in self._get_all_timezones() if tz.startswith('Africa/')],
            'America': [tz for tz in self._get_all_timezones() if tz.startswith('America/')],
            'Asia': [tz for tz in self._get_all_timezones() if tz.startswith('Asia/')],
            'Atlantic': [tz for tz in self._get_all_timezones() if tz.startswith('Atlantic/')],
            'Australia': [tz for tz in self._get_all_timezones() if tz.startswith('Australia/')],
            'Europe': [tz for tz in self._get_all_timezones() if tz.startswith('Europe/')],
            'Indian': [tz for tz in self._get_all_timezones() if tz.startswith('Indian/')],
            'Pacific': [tz for tz in self._get_all_timezones() if tz.startswith('Pacific/')],
        }

    def _get_all_timezones(self):
        """Get list of all available timezones."""
        # Using a curated list of timezones from the provided data
        timezones = []
        with open(Path(__file__).parent / 'timezone_data.txt', 'r') as f:
            for line in f:
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        timezone = parts[3].strip()
                        if timezone != 'Timezone Identifier':  # Skip header
                            timezones.append(timezone)
        return sorted(list(set(timezones)))

    def select_timezone(self):
        """Interactive timezone selection using arrow keys."""
        # First select region
        title = 'Please choose your region (press ENTER to select):'
        region_options = sorted(self.regions.keys())
        region, _ = pick(region_options, title)

        # Then select specific timezone
        title = f'Please choose your timezone in {region} (press ENTER to select):'
        timezone_options = sorted(self.regions[region])
        timezone, _ = pick(timezone_options, title)

        return timezone

    def update_settings(self, project_name, timezone):
        """Update Django settings.py with selected timezone."""
        settings_path = Path.cwd() / project_name / "settings.py"
        with open(settings_path, "r") as file:
            content = file.readlines()

        for i, line in enumerate(content):
            if line.startswith('TIME_ZONE = '):
                content[i] = f'TIME_ZONE = "{timezone}"\n'
                break

        with open(settings_path, "w") as file:
            file.writelines(content)