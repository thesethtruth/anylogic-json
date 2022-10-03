import dataclasses
from dataclasses import dataclass
import random
import json


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


HOUSE_TYPES = ["villa", "appartment", "terraced house"]
HEATING_TYPES = ["boiler", "heatpump", "hybrid heatpump"]


@dataclass
class Household:
    house_type: str
    heating_type: str
    number_of_residents: int


number_of_households = 8
output = []
for i in range(number_of_households):

    output.append(
        Household(
            house_type=random.choice(HOUSE_TYPES),
            heating_type=random.choice(HEATING_TYPES),
            number_of_residents=random.randint(1, 6),
        )
    )


str = json.dumps(output, cls=EnhancedJSONEncoder)
# str = str.replace('"', r"\"")
# str = '"' + str + '"'
with open("custom_input.txt", "w") as outfile:
    outfile.writelines([str])
