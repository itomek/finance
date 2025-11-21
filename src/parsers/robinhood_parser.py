import pandas as pd
from datetime import datetime
from typing import List
from src.parsers.base_parser import BaseParser, TransactionData

class RobinhoodParser(BaseParser):
    def parse(self, file_path: str) -> List[TransactionData]:
        # Robinhood often provides CSVs, but if PDF, we'd use camelot
        if file_path.endswith('.csv'):
            return self._parse_csv(file_path)
        else:
            # Placeholder for PDF parsing
            return []

    def _parse_csv(self, file_path: str) -> List[TransactionData]:
        df = pd.read_csv(file_path)
        transactions = []
        
        # Assuming standard Robinhood CSV export format
        # Activity Date, Process Date, Settle Date, Instrument, Description, Trans Code, Quantity, Price, Amount
        for _, row in df.iterrows():
            try:
                date_str = str(row.get('Activity Date', ''))
                if not date_str:
                    continue
                    
                date = datetime.strptime(date_str, "%Y-%m-%d") # Adjust format as needed
                amount = float(str(row.get('Amount', '0')).replace('$', '').replace(',', ''))
                desc = str(row.get('Description', ''))
                
                transactions.append(TransactionData(
                    date=date,
                    amount=amount,
                    description=desc
                ))
            except (ValueError, KeyError):
                continue
                
        return transactions

    def validate(self, transactions: List[TransactionData]) -> bool:
        return True
