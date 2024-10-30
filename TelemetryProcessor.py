from enum import IntEnum

DATA_LENGTH_IDX: int = 1
DATA_TLM_ID_IDX: int = 2

U32_LEN: int         = 4

class TelemetryEnum(IntEnum):
    GPIO_STATUS = 0x00,
    TIME_STATUS = 0x01


class GPIOStatus:
    def __init__(self, data):
        self._data = data
        self._map = \
                {
                    2: 0,
                    3: 0,
                    4: 0,
                    14: 0,
                    15: 0,
                    17: 0,
                    18: 0,
                    27: 0,
                    22: 0,
                    23: 0,
                    24: 0,
                    10: 0,
                    9: 0,
                    25: 0,
                    11: 0,
                    8: 0,
                    7: 0,
                    5: 0,
                    6: 0,
                    12: 0,
                    13: 0,
                    19: 0,
                    16: 0,
                    26: 0,
                    20: 0,
                    21: 0
                }

        self.update_status()

    def update_status(self):
        sorted_map = sorted(self._map)
        
        idx = 0
        
        for key in sorted_map:
            self._map[key] = self._data[idx]
            idx += 1
        
            print("GPIO", key, ":", self._map[key])

        print()

class TimeStatus:
    def __init__(self, data):
        self._data = data
        self._elapsed_time = 0

        self.update_time_status(self._data)

    def update_time_status(self, data):
        self._elapsed_time = int.from_bytes(data[0: U32_LEN], "big")

        print("Elapsed time: ", self._elapsed_time)


class TelemetryProcessor:

    def __init__(self):
        self._handler_map = \
                {
                    TelemetryEnum.GPIO_STATUS: self.process_gpio_status,
                    TelemetryEnum.TIME_STATUS: self.process_time_status
                }


    def process_data(self, data):
        if len(data) > 0:
            if self.is_valid_tlm(data):
                self.handle_tlm(data) 

            else:
                print("TelemetryProcessor: Received invalid data")

            

        else:
            print("TelemetryProcessor: Received invalid data length")


    def process_gpio_status(self, data):
        data_len = data[DATA_LENGTH_IDX]
        tlm_id = data[DATA_TLM_ID_IDX]

        print("TelemetryProcessor: Received TLM w/ ID of: ", tlm_id)
        
        GPIOStatus(data[DATA_TLM_ID_IDX + 1: -1])

    def process_time_status(self, data):
        tlm_id = data[DATA_TLM_ID_IDX]

        print("TelemetryProcessor: Received TLM w/ ID of: ", tlm_id)

        TimeStatus(data[DATA_TLM_ID_IDX + 1: -1])


    def handle_tlm(self, data):
        tlm_id = TelemetryEnum(data[DATA_TLM_ID_IDX])
        self._handler_map[tlm_id](data)


    def is_valid_tlm(self, data) -> bool:
        try:
            TelemetryEnum(data[DATA_TLM_ID_IDX])
            return True
        except ValueError:
            return False



