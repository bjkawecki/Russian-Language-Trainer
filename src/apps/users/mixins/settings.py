class SettingsMixin:
    def convert_to_minutes(self, steps, units):
        unit_multipliers = {
            "Minute(n)": (1, 59),
            "Stunde(n)": (60, 23 * 60),
            "Tag(e)": (1440, None),  # Keine Begrenzung für Tage
        }

        steps_as_minutes = []
        for step, unit in zip(steps, units):
            if unit in unit_multipliers:
                multiplier, max_value = unit_multipliers[unit]
                step_in_minutes = step * multiplier
                steps_as_minutes.append(
                    min(step_in_minutes, max_value) if max_value else step_in_minutes
                )

        return steps_as_minutes
