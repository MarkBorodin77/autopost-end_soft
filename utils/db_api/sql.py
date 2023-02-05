import json
import sqlite3


class Sqlite:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    async def update_tables_sql(self, state):
        state_data = await state.get_data()

        account_name = state_data["account_name"]
        account_chats = state_data["account_chats"]
        table_name = f"{account_name}_chats_table"
        # account_chats = [{}, {}]

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
    id         INTEGER PRIMARY KEY AUTOINCREMENT
                       NOT NULL,
    chat_id    INTEGER UNIQUE
                       NOT NULL,
    chat_title TEXT    NOT NULL,
    time       TEXT    DEFAULT ('["10:00"]') 
                       NOT NULL,
    work       BOOLEAN DEFAULT (False) 
                       NOT NULL,
    text       TEXT    DEFAULT [Привет, это тестовый текст, не обращай на него внимания.]
                       NOT NULL,
    photo_id   TEXT    NOT NULL
                       DEFAULT ('["None"]') 
);""")

        all_db_chats = self.cursor.execute(f"SELECT chat_id FROM {table_name}").fetchall()

        for array in account_chats:
            for chat_id in array.keys():
                if len(self.cursor.execute(f"SELECT * FROM {table_name} WHERE chat_id=?;", [chat_id]).fetchall()) == 0:
                    chat_title = array[chat_id]
                    photo_id = json.dumps(["None"])
                    #print(chat_title, chat_id)
                    self.cursor.execute(f"INSERT INTO {table_name}(chat_id, chat_title, photo_id) VALUES(?, ?, ?);",
                                        [chat_id, chat_title, photo_id])

                    self.conn.commit()

        for db_chat in all_db_chats:
            db_chat_id = db_chat[0]

            in_account_chats = False

            for array in account_chats:
                for chat_id in array.keys():
                    if db_chat_id == chat_id:
                        in_account_chats = True
                        break

            if in_account_chats == False:
                self.cursor.execute(f"DELETE FROM {table_name} WHERE chat_id=?", [db_chat_id])

        self.conn.commit()

    async def update_text_sql(self, state, text):
        state_data = await state.get_data()

        selected_chats = state_data["selected_chats"]
        account_name = state_data["account_name"]
        account_chats = state_data["account_chats"]
        table_name = f"{account_name}_chats_table"

        for chat_id in selected_chats.keys():
            self.cursor.execute(f"UPDATE {table_name} SET text=? WHERE chat_id=?", [text, chat_id])

        self.conn.commit()

    async def update_time_sql(self, state, time):
        state_data = await state.get_data()

        selected_chats = state_data["selected_chats"]
        account_name = state_data["account_name"]
        account_chats = state_data["account_chats"]
        table_name = f"{account_name}_chats_table"

        time = json.dumps(time)

        for chat_id in selected_chats.keys():
            self.cursor.execute(f"UPDATE {table_name} SET time=? WHERE chat_id=?", [time, chat_id])

        self.conn.commit()

    async def mute_chats_sql(self, state):
        state_data = await state.get_data()

        selected_chats = state_data["selected_chats"]
        account_name = state_data["account_name"]
        table_name = f"{account_name}_chats_table"

        for chat_id in selected_chats.keys():
            self.cursor.execute(f"UPDATE {table_name} SET work=? WHERE chat_id=?", [0, chat_id])

        self.conn.commit()

    async def enable_chats_sql(self, state):
        state_data = await state.get_data()

        selected_chats = state_data["selected_chats"]
        account_name = state_data["account_name"]
        table_name = f"{account_name}_chats_table"

        for chat_id in selected_chats.keys():
            self.cursor.execute(f"UPDATE {table_name} SET work=? WHERE chat_id=?;", [1, chat_id])

        self.conn.commit()

    async def get_working_chats_sql(self, state):
        state_data = await state.get_data()

        account_name = state_data["account_name"]
        table_name = f"{account_name}_chats_table"

        chats_data = self.cursor.execute(f"SELECT chat_id, chat_title, time, text, photo_id FROM {table_name} WHERE work=1;")

        return chats_data.fetchall()

    async def get_all_chats_sql(self, state):
        state_data = await state.get_data()

        account_name = state_data["account_name"]
        table_name = f"{account_name}_chats_table"

        chats_data = self.cursor.execute(f"SELECT chat_id, chat_title, time, text, photo_id FROM {table_name};")

        return chats_data.fetchall()

    async def get_one_chat_sql(self, account_name, chat_id):
        table_name = f"{account_name}_chats_table"

        chats_data = self.cursor.execute(f"SELECT * FROM {table_name} WHERE chat_id=?;", [chat_id]).fetchall()

        for chat_data in chats_data:
            return chat_data

    async def add_photo_sql(self, state, photo_unique_id):
        state_data = await state.get_data()

        selected_chats = state_data["selected_chats"]
        account_name = state_data["account_name"]
        account_chats = state_data["account_chats"]
        table_name = f"{account_name}_chats_table"



        for chat_id in selected_chats.keys():
            chat_data = await self.get_one_chat_sql(account_name, chat_id)

            photo_id = json.loads(chat_data[6])

            if str(photo_id[0]) == "None":
                photo_id = json.dumps([str(photo_unique_id)])
            else:
                photo_id.append(photo_unique_id)
                photo_id = json.dumps(photo_id)

            self.cursor.execute(f"UPDATE {table_name} SET photo_id=? WHERE chat_id=?", [photo_id, chat_id])

        self.conn.commit()

    async def delete_photo_sql(self, state):
        state_data = await state.get_data()

        selected_chats = state_data["selected_chats"]
        account_name = state_data["account_name"]
        table_name = f"{account_name}_chats_table"



        for chat_id in selected_chats.keys():
            photo_id = json.dumps(["None"])

            self.cursor.execute(f"UPDATE {table_name} SET photo_id=? WHERE chat_id=?", [photo_id, chat_id])

        self.conn.commit()