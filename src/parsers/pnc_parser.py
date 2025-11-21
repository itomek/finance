import camelot
import pandas as pd
from datetime import datetime
from typing import List
from src.parsers.base_parser import BaseParser, TransactionData

class PNCParser(BaseParser):
    def parse(self, file_path: str) -> List[TransactionData]:
        # Extract tables from PDF
        tables = camelot.read_pdf(file_path, pages='all', flavor='stream')
        
        transactions = []
        for table in tables:
            df = table.df
            # Basic logic to identify transaction rows - this will need refinement based on actual PNC PDF structure
            # Assuming columns: Date, Description, Withdrawal, Deposit, Balance
            for _, row in df.iterrows():
                try:
                    # Placeholder logic - needs actual template matching
                    date_str = str(row[0])
                    desc = str(row[1])
                    withdrawal = str(row[2])
                    deposit = str(row[3])
                    
                    # Skip header rows or empty rows
                    if not self._is_date(date_str):
                        continue
                        
                    date = datetime.strptime(date_str, "%m/%d/%Y")
                    
                    amount = 0.0
                    if withdrawal and withdrawal.strip():
                        amount = -float(withdrawal.replace('$', '').replace(',', ''))
                    elif deposit and deposit.strip():
                        amount = float(deposit.replace('$', '').replace(',', ''))
                    
                    if amount != 0:
                        transactions.append(TransactionData(
                            date=date,
                            amount=amount,
                            description=desc
                        ))
                except (ValueError, IndexError):
                    continue
                    
        return transactions

    def validate(self, transactions: List[TransactionData]) -> bool:
        # Implement balance reconciliation logic here
        return True

    def _is_date(self, string: str) -> bool:
        try:
            datetime.strptime(string, "%m/%d/%Y")
            return True
        except ValueError:
            return False
