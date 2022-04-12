from . import PerrenoudEnum
from .model import AppEnum, PerrenoudEnumKind


class AppEnumService:
    @staticmethod
    def get_enums(
        enum_list,
    ):
        output = dict()
        if enum_list:
            items = (
                AppEnum.query.filter(AppEnum.kind.in_(enum_list))
                .filter(AppEnum.disabled.isnot(True))
                .order_by(AppEnum.kind.asc(), AppEnum.display_order.asc())
                .all()
            )
            for item in items:
                if item.kind not in output:
                    output[item.kind] = []
                output[item.kind].append(item.name)

        return output


class PerrenoudAppEnumService:
    @staticmethod
    def get_perrenoud_enums(enums_list):
        enums = []
        for enum in enums_list:
            new_perrenoud_items = PerrenoudEnum.query.filter(
                PerrenoudEnum.index == enum
            ).all()
            name = (
                PerrenoudEnumKind.query.filter(PerrenoudEnumKind.index == enum)
                .first()
                .label
            )
            enums.append({"index": enum, "name": name, "items": new_perrenoud_items})
        return enums
