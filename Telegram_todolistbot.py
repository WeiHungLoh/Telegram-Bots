import psycopg2
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

bot_token = "REPLACE_WITH_YOUR_BOT_TOKEN"

# Establish database connection details
db_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="REPLACE_WITH_YOUR_PASSWORD",
    host="localhost",
    port="5432"
)

def create_tables():
    with db_conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            current_index INTEGER NOT NULL,
            user_id BIGINT NOT NULL,
            description TEXT NOT NULL,
            PRIMARY KEY(current_index, user_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        db_conn.commit()

# List down commands for users to call
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to the ToDoList Bot! \n\nThe commands are as follows: \n"
                                    "1) /add <task_desc> to add a task \n"
                                    "2) /remove <task_index> to remove a task \n"
                                    "3) /removeall to remove all tasks \n"
                                    "4) /viewtasks to view current tasks \n")

async def addtask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    if context.args:
        user_id = update.message.from_user.id
        description = " ".join(context.args)

        with db_conn.cursor() as cur:
            # Since index is incremented once a task is added, MAX() will retrieve latest index
            cur.execute("SELECT MAX(current_index) FROM tasks WHERE user_id = %s", (user_id,))
            result = cur.fetchone()

            if result[0]:
                # If user exists, increment their current index
                current_index = result[0]
                new_index = current_index + 1
                cur.execute("INSERT INTO tasks (current_index, user_id, description) VALUES (%s, %s, %s)", (new_index, user_id, description))
            else:
                # If user does not exist, initialize their index at 1
                new_index = 1
                cur.execute("INSERT INTO tasks (current_index, user_id, description) VALUES (%s, %s, %s)", (new_index, user_id, description))
            
            db_conn.commit()
        
        await update.message.reply_text(f"{new_index}. {description} added successfully")
    else:
        await update.message.reply_text("Please provide a task description")

async def removetask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        try:
            task_id = int(context.args[0])
            user_id = update.message.from_user.id
            
            with db_conn.cursor() as cur:
                # Remove a particular data from the user
                cur.execute(
                    "DELETE FROM tasks WHERE user_id = %s AND current_index = %s RETURNING current_index",
                    (user_id, task_id)
                )
                result = cur.fetchone()
                if result:
                    cur.execute(
                        "SELECT current_index, description FROM tasks WHERE user_id = %s ORDER BY current_index",
                        (user_id,)
                    )
                    tasks = cur.fetchall()
                    # Remove all existing data from the user
                    cur.execute("DELETE FROM tasks WHERE user_id = %s", (user_id,))
                    
                    # Re-order index of existing data from the user
                    new_index = 1
                    for i, desc in tasks:
                        cur.execute(
                            "INSERT INTO tasks (current_index, user_id, description) VALUES (%s, %s, %s)",
                            (new_index, user_id, desc)
                        )
                        new_index += 1
                               
                    db_conn.commit()
                    
                    await update.message.reply_text(f"Task {task_id} has been successfully removed")
                else:
                    await update.message.reply_text(f"Task {task_id} does not exist")
        except ValueError:
            await update.message.reply_text("Please provide a valid task ID")
    else:
        await update.message.reply_text("Please provide a task ID to remove")

async def removeall(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    with db_conn.cursor() as cur:
        cur.execute("DELETE FROM tasks WHERE user_id = %s", (user_id,))
        db_conn.commit()
    
    await update.message.reply_text("All tasks have been cleared")

async def viewtasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    with db_conn.cursor() as cur:
        cur.execute("SELECT current_index, description FROM tasks WHERE user_id = %s ORDER BY current_index", (user_id,))
        tasks = cur.fetchall()
    
    if tasks:
        response = '\n'.join([f"{i}. {desc}" for i, desc in tasks])
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("No tasks available")

# Function will be executed when commands not listed have been called
async def handletext(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I didn't recognize that command. Please type /start to check the available commands")

def main() -> None:
    # Create the necessary tables
    create_tables()

    # Create the telegram bot
    application = Application.builder().token(bot_token).build()

    # Handle commands called on Telegram Bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", addtask))
    application.add_handler(CommandHandler("remove", removetask))
    application.add_handler(CommandHandler("removeall", removeall))
    application.add_handler(CommandHandler("viewtasks", viewtasks))
    application.add_handler(MessageHandler(~filters.COMMAND, handletext))

    application.run_polling()

if __name__ == '__main__':
    main()
