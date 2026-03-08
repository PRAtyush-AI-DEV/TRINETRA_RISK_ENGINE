from database.db_setup import engine, Base
# Models ko import karna zaroori hai tabhi Base ko pata chalega ki kya banana hai

print("⏳ Neon Cloud par 'trades' table ban rahi hai...")

# Ye aakhri command hai jo cloud par jaakar tables create karegi
Base.metadata.create_all(bind=engine)

print("✅ SUCCESS: Teri Cloud Tijori ab data lene ke liye taiyar hai!")