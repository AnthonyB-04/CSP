import random

days = ["Пн", "Вт", "Ср", "Чт", "Пт"]

disciplines_count = {
    0: 2,
    1: 1,
    2: 1,
    3: 2,
    4: 1,
    5: 2,
    6: 2,
    7: 1,
    8: 1,
    9: 2,
}

disciplines = [
    "Iнформаційні технології в менеджментi",
    "Вибрані розділи трудового права і основ підприємницької діяльності",
    "Розробка програмного забезпечення",
    "Лаб. Розробка програмного забезпечення",
    "ОС з розподілом часу",
    "Проблеми штучного інтелекту",
    "Нейронні мережі",
    "Лаб. Нейронні мережі",
    "Інтелектуальні системи",
    "Лаб. Інтелектуальні системи",
]

teachers = range(0, 9)

teacher_disciplines = [{0}, {1}, {2, 3}, {4}, {5}, {6, 7}, {8}, {9}, {9}]

num_days = len(days)
num_classes = 3
num_classes_total = num_days * num_classes

num_teachers = len(teachers)
num_disciplines = len(disciplines)


class CSP:
    def __init__(self):
        self.disciplines_index = set(range(num_disciplines))

        self.subject_assignments = [None for _ in range(num_classes_total)]

        self.teacher_assignments = [None for _ in range(num_classes_total)]

        self.checks = 0

    def constraints(self):
        self.checks += 1

        for lesson, teacher in enumerate(self.teacher_assignments):
            if teacher is not None and self.subject_assignments[lesson] not in teacher_disciplines[self.teacher_assignments[lesson]]:
                return False

        subjects = [x for x in self.subject_assignments if x is not None]

        for s in subjects:
            if len([x for x in self.subject_assignments if x == s]) > disciplines_count[s]:
                return False

        for i in range(len(self.teacher_assignments) - num_classes + 1):
            window = self.teacher_assignments[i:i+num_classes]
            counts = {}
            for item in window:
                counts[item] = counts.get(item, 0) + 1
                if counts[item] > num_classes - 1 and item is not None:
                    return False

        for i in range(len(self.subject_assignments) - num_classes + 1):
            window = self.subject_assignments[i:i+num_classes]
            counts = {}
            for item in window:
                counts[item] = counts.get(item, 0) + 1
                if counts[item] > num_classes - 1 and item is not None:
                    return False

        return True

    def heuristic(self):
        unassigned = []
        for lesson in range(num_classes_total):
            unassigned.append(sum([self.teacher_assignments[lesson] is None]))
        lesson = unassigned.index(max(unassigned))
        if self.teacher_assignments[lesson] is None:
            return lesson

    def domain(self):
        for teacher in random.sample(range(num_teachers), num_teachers):
            available_classes = list(
                self.disciplines_index.intersection(teacher_disciplines[teacher]))
            for subject in random.sample(available_classes, len(available_classes)):
                yield teacher, subject

    def backtracking(self):
        print(f"{self.checks}\n")
        lesson = self.heuristic()

        if lesson is None:
            return True

        for teacher, subject in self.domain():
            self.teacher_assignments[lesson] = teacher
            self.subject_assignments[lesson] = subject

            if self.constraints():
                res = self.backtracking()
                if res:
                    return True
            self.teacher_assignments[lesson] = None
            self.subject_assignments[lesson] = None

        return False

    def print(self):
        for d in range(num_days):
            print(f"\n{days[d]}")
            for l in range(num_classes):
                l = d * num_classes + l
                lesson = (
                    f"{disciplines[self.subject_assignments[l]]} {teachers[self.teacher_assignments[l]]}")
                print(f"{l + 1}: {lesson}")


csp = CSP()
csp.backtracking()
csp.print()
