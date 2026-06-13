from Utilities.customLogger import LogGen
import pytest


class TestDatabaseFullSuite:
    logger = LogGen.loggen()

    def test_1_verify_all_tables_exist(self):
        """Check karna ki kya public schema mein hamari zaroori Django tables maujood hain"""
        cursor = self.db.cursor()
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        all_tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        
        self.logger.info(f"\n📊 [DB LOG] Tables found in Database: {all_tables}")
        
        # SSERTS (Aapke Real Database Ke Tables Ke Hisab Se)
        assert len(all_tables) > 0, "❌ FAILED: Database ekdum khali hai!"
        
        #Humne yahan table ke sahi Django names daal diye hain:
        assert "users_user" in all_tables, "❌ FAILED: 'users_user' table missing hai!"
        assert "products_product" in all_tables, "❌ FAILED: 'products_product' table missing hai!"
        assert "order_order" in all_tables, "❌ FAILED: 'order_order' table missing hai!"
        
        self.logger.info("🟢 SUCCESS: Schema validation passed! Saari Django tables exist karti hain.")