import json
from typing import Optional, Dict

from ape.api import BlockAPI, EcosystemAPI, ReceiptAPI, TransactionAPI, TransactionType
from ape.contracts import ContractLog
from ape.types import AddressType
from ethpm_types import ABI


class DemoTransaction(TransactionAPI):
    """
    A transaction that is basically a mock.
    """

    message_data = {}

    def encode(self) -> bytes:
        return json.dumps(self.message_data).encode()


class DemoReceipt(ReceiptAPI):
    """
    A receipt that is basically a mock.
    """

    @classmethod
    def decode(cls, data: dict) -> "ReceiptAPI":
        return cls(**data)


class DemoBlock(BlockAPI):
    """
    A block that is basically a mock.
    """

    @classmethod
    def decode(cls, data: Dict) -> "BlockAPI":
        return cls(**data)


class DemoEcosystem(EcosystemAPI):
    """
    An ecosystem that is basically a mock.
    """

    transaction_types = {
        TransactionType.STATIC: DemoTransaction,
        TransactionType.DYNAMIC: DemoTransaction
    }
    receipt_class = DemoReceipt
    block_class = DemoBlock

    def encode_deployment(
        self, deployment_bytecode: bytes, abi: Optional[ABI], *args, **kwargs
    ) -> TransactionAPI:
        txn = self.create_transaction(**kwargs)
        txn.message_data["deployment_bytecode"] = deployment_bytecode
        txn.message_data["abi"] = abi
        return txn

    def encode_transaction(self, address: AddressType, abi: ABI, *args, **kwargs) -> TransactionAPI:
        txn = DemoTransaction(*args, **kwargs)
        txn.message_data["address"] = address
        txn.message_data["abi"] = abi
        return txn

    def decode_event(self, abi: ABI, receipt: ReceiptAPI) -> ContractLog:
        name = abi.name
        return ContractLog(name, {})

    def create_transaction(self, **kwargs) -> TransactionAPI:
        return DemoTransaction(**kwargs)
