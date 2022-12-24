class Pid():
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.max_i_output = 0
        self.max_err = 0
        self.err_sum = 0
        self.max_output = 0
        self.min_output = 0
        self.target = 0
        self.last_actual = 0
        self.first_run = True
        self.output_ramp_rate = 0
        self.last_output = 0
        self.target_range = 0

    def set_MaxIOutput(self, maximum):
        self.max_i_output = maximum
        if self.i != 0:
            self.max_err = self.max_i_output / self.i

    @staticmethod
    def bounded(value, min, max):
        return min < value < max

    @staticmethod
    def saturation(value, min, max):
        if value > max:
            return max
        elif value > min:
            return value
        else:
            return min

    def set_Output_Limits(self, minimum, maximum):
        if maximum < minimum:
            return
        self.max_output = maximum
        self.min_output = minimum

        if self.max_i_output == 0 or self.max_i_output > (maximum - minimum):
            self.set_MaxIOutput(maximum - minimum)

    def getOutput(self, actual, target):

        self.target = target

        if self.target_range != 0:
            target = self.saturation(target, actual - self.target_range, actual + self.target_range)

        error = target - actual
        p_output = self.p * error

        if self.first_run:
            self.last_output = actual
            self.last_output = p_output
            self.first_run = False

        d_output = -self.d * (actual - self.last_actual)
        self.last_actual = actual

        i_output = self.i * self.err_sum
        if self.max_i_output != 0:
            i_output = self.saturation(i_output, -self.max_i_output, self.max_i_output)

        output = p_output + i_output + d_output

        if self.min_output != self.max_i_output and not self.bounded(output, self.min_output, self.max_i_output):
            self.err_sum = error

        elif self.output_ramp_rate != 0 and not self.bounded(output, self.last_output - self.output_ramp_rate,
                                                             self.last_output + self.output_ramp_rate):
            self.err_sum = error


        elif self.max_i_output != 0:
            self.err_sum = self.saturation(self.err_sum + error, -self.max_err, self.max_err)

        else:
            self.err_sum += error

        if self.output_ramp_rate != 0:
            output = self.saturation(output, self.last_output - self.output_ramp_rate,
                                     self.last_output + self.output_ramp_rate)

        if self.min_output != self.max_output:
            output = self.saturation(output, self.min_output, self.max_output)

        self.last_output = output
        return output

    def getOutputEmpty(self):
        return self.getOutput(self.last_actual, self.target)

    def getOutputActual(self, actual):
        return self.getOutput(actual, self.target)
