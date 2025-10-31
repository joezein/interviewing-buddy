"""Interview templates registry."""

from .soal_labs_full_stack import TEMPLATE as SOAL_LABS_FULL_STACK_TEMPLATE


TEMPLATES = {SOAL_LABS_FULL_STACK_TEMPLATE["id"]: SOAL_LABS_FULL_STACK_TEMPLATE}


__all__ = ["TEMPLATES", "SOAL_LABS_FULL_STACK_TEMPLATE"]
