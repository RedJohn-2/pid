import matplotlib.pyplot as plt
import numpy as np
from Pid import Pid

if __name__ == '__main__':
    fig, ax = plt.subplots(3)

    x = np.linspace(0, 10, 600)
    y_target = np.zeros(600)
    for i in range(600):
        if i < 120:
            y_target[i] = 50
        elif i < 300:
            y_target[i] = 70
        elif i < 500:
            y_target[i] = 20
        else:
            y_target[i] = 50

    y_actual = np.zeros(600)
    pid = Pid(0.14, 0.001, 0.3)
    target = 50
    actual = 0
    output = 0
    pid.target = target

    for i in range(600):
        if i == 120:
            target = 70
        if i == 300:
            target = 20
        if i == 500:
            target = 50

        output = pid.getOutput(actual, target)
        actual += output
        y_actual[i] = actual

    y_error = y_target - y_actual
    fig.tight_layout(h_pad=2)
    ax[0].plot(x, y_target)
    ax[0].set_title('Желаемый уровень воды в барабане')
    ax[1].plot(x, y_actual)
    ax[1].set_title('Текущий уровень воды в барабане')
    ax[2].plot(x, y_error)
    ax[2].set_title('Ошибка')
    plt.show()
