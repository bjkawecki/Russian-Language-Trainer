from apps.users.models import Step


class SettingsStepsServices:
    @staticmethod
    def get_steps_as_strings(user):
        steps = list(Step.objects.filter(user=user).values_list("step", flat=True))
        if not steps:
            steps = [10, 60, 1440]
        steps.sort()
        string_steps = []
        for step in steps:
            if step < 60:
                string_steps.append(f"{step} {'Minuten' if step > 1 else 'Minute'}")
            elif 1440 > step and step >= 60:
                string_steps.append(
                    f"{step // 60} {'Stunden' if step > 60 else 'Stunde'}"
                )
            elif step >= 1440:
                string_steps.append(
                    f"{step // 1440} {'Tage' if step > 1440 else 'Tag'}"
                )
        return string_steps

    @staticmethod
    def get_steps(user):
        steps = list(Step.objects.filter(user=user).values_list("step", flat=True))
        if not steps:
            steps = [10, 60, 1440]
        steps.sort()
        unit_steps = []

        for step in steps:
            if step < 60:
                unit_steps.append((step, "Minute(n)"))
            elif step in range(60, 1439):
                unit_steps.append((step // 60, "Stunde(n)"))
            elif step >= 1440:
                unit_steps.append((step // 1440, "Tag(e)"))
        return unit_steps

    @staticmethod
    def save_steps(user, steps_as_minutes):
        Step.objects.filter(user=user).delete()
        for step in steps_as_minutes:
            Step.objects.filter(user=user).create(step=step, user=user)
