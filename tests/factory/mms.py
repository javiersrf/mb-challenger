import factory
from factory import Faker
from src.core.models.mms import MMsModel


class MMsModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MMsModel

    pair = Faker("random_element", elements=["BRLETH", "BRLBTC"])
    timestamp = Faker("unix_time")
    mms_20 = Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    mms_50 = Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    mms_200 = Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
