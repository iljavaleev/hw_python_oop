from dataclasses import dataclass, asdict
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ("Тип тренировки: {training_type}; "
               "Длительность: {duration:.3f} ч.; "
               "Дистанция: {distance:.3f} км; "
               "Ср. скорость: {speed:.3f} км/ч; "
               "Потрачено ккал: {calories:.3f}.")

    def get_message(self):
        """Насчет элегантности не знаю."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weigth = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type=training_type,
                           duration=duration,
                           distance=distance,
                           speed=speed,
                           calories=calories)


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        minutes = hours_to_minutes(self.duration)
        part1 = (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
        return part1 * self.weigth / self.M_IN_KM * minutes


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        minutes = hours_to_minutes(self.duration)
        part1 = (self.get_mean_speed() ** 2 // self.height)
        return (coeff_calorie_1 * self.weigth + part1
                * coeff_calorie_2 * self.weigth) * minutes


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        part1 = (self.get_mean_speed() + coeff_calorie_1)
        return part1 * coeff_calorie_2 * self.weigth


def hours_to_minutes(time):
    """Переводит время из часов в минуты."""
    return time * 60


class WorkoutNotFoundException(Exception):
    """Custom exception. Не стал выносить в отдельный модуль."""


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict: Dict[str, Type[Training]] = ({'SWM': Swimming, 'RUN': Running,
                                             'WLK': SportsWalking})
    if workout_type not in type_dict:
        raise WorkoutNotFoundException(f'This workout type {workout_type} '
                                       f'doesn\'t exist')
    return type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
