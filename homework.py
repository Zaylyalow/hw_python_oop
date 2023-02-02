from dataclasses import asdict, dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TEXT: str = ('Тип тренировки: {training_type}: '
                 'Длительность: {duration:.3f} ч, '
                 'Дистанция: {distance:.3f} км, '
                 'Ср. скорость: {speed:.3f} км/ч, '
                 'Потрачено ккал: {calories:.3f}. ')

    def get_message(self) -> str:
        return self.TEXT.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    MIN_IN_HOUR = 60
    M_IN_KM = 1000
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Необходимо переопределить метод")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_1 = 18
    CALORIES_MEAN_SPEED_2 = 1.79
    LEN_STEP = 0.65
    action: int
    duration: float
    weight: float

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_1 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_1 = 0.035
    CALORIES_MEAN_SPEED_2 = 0.029
    KMH_TO_MH = 0.278
    S_IN_M = 100
    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_1 * self.weight
                 + ((self.get_mean_speed() * self.KMH_TO_MH) ** 2
                    / self.height * self.S_IN_M)
                 * self.CALORIES_MEAN_SPEED_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_1 = 1.1
    CALORIES_MEAN_SPEED_2 = 2
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_1)
                * self.CALORIES_MEAN_SPEED_2
                * self.weight * self.duration)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_workout: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}

    if workout_type not in types_workout:
        raise ValueError("Такого кода не существует")

    return types_workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180]), ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
