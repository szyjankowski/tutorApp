from django.db import models
from users.models import CustomUser
from model_utils import Choices

TRANSACTION_TYPES = Choices(
    (1, "TRANSFER", "Transfer"),
)


class Wallet(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.email} - Balance: {self.balance}"


class Transaction(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_transactions"
    )
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_transactions"
    )
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Transaction {self.id} - {self.get_transaction_type_display()} -"
            f" {self.amount} from {self.sender} to {self.receiver}"
        )
