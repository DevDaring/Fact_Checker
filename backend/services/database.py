import pandas as pd
import json
from datetime import datetime
from typing import Optional, List, Dict
from pathlib import Path
from config.settings import settings

class Database:
    """CSV-based database operations"""

    @staticmethod
    def _ensure_file_exists(file_path: Path, headers: List[str]):
        """Ensure CSV file exists with headers"""
        if not file_path.exists():
            df = pd.DataFrame(columns=headers)
            df.to_csv(file_path, index=False)

    @staticmethod
    def _read_csv(file_path: Path) -> pd.DataFrame:
        """Read CSV file"""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return pd.DataFrame()

    @staticmethod
    def _write_csv(df: pd.DataFrame, file_path: Path):
        """Write DataFrame to CSV"""
        df.to_csv(file_path, index=False)

    # ============= USER OPERATIONS =============

    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict]:
        """Get user by email"""
        df = Database._read_csv(settings.USERS_CSV)
        if df.empty:
            return None

        user = df[df['email'] == email]
        if user.empty:
            return None

        # Replace NaN with empty strings
        user = user.fillna('')

        return user.iloc[0].to_dict()

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        df = Database._read_csv(settings.USERS_CSV)
        if df.empty:
            return None

        user = df[df['user_id'] == user_id]
        if user.empty:
            return None

        # Replace NaN with empty strings
        user = user.fillna('')

        return user.iloc[0].to_dict()

    @staticmethod
    def create_user(email: str, password_hash: str, role: str) -> Dict:
        """Create a new user"""
        df = Database._read_csv(settings.USERS_CSV)

        # Get next user_id
        user_id = 1 if df.empty else int(df['user_id'].max()) + 1

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user = {
            'user_id': user_id,
            'email': email,
            'password_hash': password_hash,
            'role': role,
            'created_at': now,
            'last_login': now
        }

        df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
        Database._write_csv(df, settings.USERS_CSV)

        return new_user

    @staticmethod
    def update_last_login(user_id: int):
        """Update user's last login timestamp"""
        df = Database._read_csv(settings.USERS_CSV)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.loc[df['user_id'] == user_id, 'last_login'] = now
        Database._write_csv(df, settings.USERS_CSV)

    @staticmethod
    def get_all_users() -> List[Dict]:
        """Get all users (for admin)"""
        df = Database._read_csv(settings.USERS_CSV)
        if df.empty:
            return []
        
        # Replace NaN with empty strings
        df = df.fillna('')
        
        return df.to_dict('records')

    # ============= FACT CHECK OPERATIONS =============

    @staticmethod
    def create_fact_check(
        user_id: int,
        upload_type: str,
        file_path: str,
        extracted_text: Optional[str],
        gemini_response: str,
        citations: List[Dict]
    ) -> Dict:
        """Create a new fact check record"""
        df = Database._read_csv(settings.FACT_CHECKS_CSV)

        # Get next fact_check_id
        fact_check_id = 1 if df.empty else int(df['fact_check_id'].max()) + 1

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_fact_check = {
            'fact_check_id': fact_check_id,
            'user_id': user_id,
            'upload_type': upload_type,
            'file_path': file_path,
            'extracted_text': extracted_text or '',
            'gemini_response': gemini_response,
            'citations': json.dumps(citations),
            'timestamp': now
        }

        df = pd.concat([df, pd.DataFrame([new_fact_check])], ignore_index=True)
        Database._write_csv(df, settings.FACT_CHECKS_CSV)

        return new_fact_check

    @staticmethod
    def get_fact_check_by_id(fact_check_id: int) -> Optional[Dict]:
        """Get fact check by ID"""
        df = Database._read_csv(settings.FACT_CHECKS_CSV)
        if df.empty:
            return None

        fact_check = df[df['fact_check_id'] == fact_check_id]
        if fact_check.empty:
            return None

        # Replace NaN with empty strings
        fact_check = fact_check.fillna('')

        result = fact_check.iloc[0].to_dict()
        # Parse citations JSON
        if result.get('citations'):
            try:
                result['citations'] = json.loads(result['citations'])
            except:
                result['citations'] = []
        else:
            result['citations'] = []

        return result

    @staticmethod
    def get_user_fact_checks(user_id: int) -> List[Dict]:
        """Get all fact checks for a user"""
        df = Database._read_csv(settings.FACT_CHECKS_CSV)
        if df.empty:
            return []

        user_checks = df[df['user_id'] == user_id]
        if user_checks.empty:
            return []

        # Sort by timestamp descending
        user_checks = user_checks.sort_values('timestamp', ascending=False)

        # Replace NaN with empty strings or appropriate defaults
        user_checks = user_checks.fillna('')

        results = user_checks.to_dict('records')
        # Parse citations for each record
        for result in results:
            if result.get('citations'):
                try:
                    result['citations'] = json.loads(result['citations'])
                except:
                    result['citations'] = []
            else:
                result['citations'] = []

        return results

    @staticmethod
    def get_all_fact_checks() -> List[Dict]:
        """Get all fact checks (for admin)"""
        df = Database._read_csv(settings.FACT_CHECKS_CSV)
        if df.empty:
            return []

        # Sort by timestamp descending
        df = df.sort_values('timestamp', ascending=False)

        # Replace NaN with empty strings or appropriate defaults
        df = df.fillna('')

        results = df.to_dict('records')
        # Parse citations for each record
        for result in results:
            if result.get('citations'):
                try:
                    result['citations'] = json.loads(result['citations'])
                except:
                    result['citations'] = []
            else:
                result['citations'] = []

        return results

    # ============= COMMENT OPERATIONS =============

    @staticmethod
    def create_comment(fact_check_id: int, admin_id: int, comment_text: str) -> Dict:
        """Create a new admin comment"""
        df = Database._read_csv(settings.ADMIN_COMMENTS_CSV)

        # Get next comment_id
        comment_id = 1 if df.empty else int(df['comment_id'].max()) + 1

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_comment = {
            'comment_id': comment_id,
            'fact_check_id': fact_check_id,
            'admin_id': admin_id,
            'comment_text': comment_text,
            'timestamp': now
        }

        df = pd.concat([df, pd.DataFrame([new_comment])], ignore_index=True)
        Database._write_csv(df, settings.ADMIN_COMMENTS_CSV)

        return new_comment

    @staticmethod
    def get_comments_by_fact_check(fact_check_id: int) -> List[Dict]:
        """Get all comments for a fact check"""
        df = Database._read_csv(settings.ADMIN_COMMENTS_CSV)
        if df.empty:
            return []

        comments = df[df['fact_check_id'] == fact_check_id]
        if comments.empty:
            return []

        # Sort by timestamp ascending
        comments = comments.sort_values('timestamp', ascending=True)

        # Replace NaN with empty strings
        comments = comments.fillna('')

        return comments.to_dict('records')

    @staticmethod
    def get_all_comments() -> List[Dict]:
        """Get all comments (for admin)"""
        df = Database._read_csv(settings.ADMIN_COMMENTS_CSV)
        if df.empty:
            return []

        # Replace NaN with empty strings
        df = df.fillna('')

        return df.to_dict('records')
