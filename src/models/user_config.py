import json
from pydantic import (
    BaseModel as pydantic_BaseModel,
)
from pydantic import (
    ConfigDict,
    Field,
    ValidationError,
    model_validator,
)
from pydantic.alias_generators import to_camel
from typing import Self


class BaseModel(pydantic_BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


class Column(pydantic_BaseModel):
    model_config = ConfigDict(extra="allow")

    DATE: str


class Data(BaseModel):
    name: str
    siqual_name: str
    worksheet_name: str
    is_raw_material: bool
    generic_position_in_list: int
    columns_to_input: Column


class File(BaseModel):
    path_abs: str
    header_row: int


class Workbook(BaseModel):
    products: File
    raw_materials: File


class Materials(BaseModel):
    workbooks: Workbook
    data: list[Data]

    def get_material_data_from_name(self, name: str) -> Data:
        for item in self.data:
            if item.name == name:
                return item

    def _get_material_names(self, is_raw_mat: bool = True) -> list[str]:
        return [item.name for item in self.data if item.is_raw_material == is_raw_mat]

    def get_product_names(self) -> list[str]:
        return self._get_material_names(is_raw_mat=False)

    def get_raw_material_names(self) -> list[str]:
        return self._get_material_names(is_raw_mat=True)


class Plant(BaseModel):
    name: str = ""
    code: str
    materials: Materials


class UserConfig(BaseModel):
    delay_between_commands: float = Field(default=0.5)
    delay_between_screens: float = Field(default=2.5)
    active_plant_code: str
    plants: list[Plant]
    active_plant: Plant | None = None

    @model_validator(mode="after")
    def check_active_plant_code_exists(self) -> None:
        for plant in self.plants:
            if plant.code == self.active_plant_code:
                self.active_plant = plant
                break

        if not self.active_plant_code:
            raise ValidationError(
                f"El codigo de la planta activa {self.active_plant_code} "
                "no coincide con ninguna de las plantas declaradas"
            )

    @classmethod
    def from_json(cls, filename: str = "config.json") -> Self:
        """Loads the json filename and initializes an instance of this class

        Parameters
        ----------
        filename : str, optional
            a filename or full path to a confi file, by default "config.json"

        Returns
        -------
        UserConfig
            An instance of UserConfig

        Raises
        ------
        ValidationError
            When there is a problem with the contents of the config file

        IOError
            When there is a problem opening the file

        """

        try:
            with open(filename, "r", encoding="utf-8") as file:
                d = json.load(file)
                return cls(**d)
        except ValidationError:
            raise ValueError(f"El archivo {filename} no tiene un formato correcto.")
        except Exception:
            raise IOError(f"No existe el archivo {filename} o hay un problema abriendolo.")
