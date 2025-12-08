from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///./items.db')

with engine.connect() as conn:
    # Count total items
    result = conn.execute(text('SELECT COUNT(*) FROM items'))
    total = result.scalar()
    print(f'Total items in database: {total}')
    
    # Show items by environment
    result = conn.execute(text('SELECT environment, COUNT(*) as count FROM items GROUP BY environment'))
    print('\nItems by environment:')
    for row in result:
        print(f'  {row[0]}: {row[1]}')
    
    # Show all items
    if total > 0:
        result = conn.execute(text('SELECT id, name, environment, description FROM items'))
        print('\nAll items:')
        for row in result:
            print(f'  ID: {row[0]}, Name: {row[1]}, Env: {row[2]}, Desc: {row[3]}')

