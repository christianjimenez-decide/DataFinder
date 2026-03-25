import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data(num_rows=5000):
    products = {
        'Electrónica': ['Laptop Pro 15', 'Monitor 27" 4K', 'Tablet Air', 'Smartphone X', 'Auriculares Noise-Cancelling'],
        'Accesorios': ['Ratón Ergonómico', 'Teclado Mecánico', 'Webcam HD', 'Cable HDMI 2.1', 'Hub USB-C'],
        'Mobiliario': ['Silla Ergonómica', 'Escritorio Elevable', 'Lámpara LED', 'Soporte Monitor'],
        'Software': ['Licencia Office', 'Antivirus Personal', 'Suscripción Cloud', 'Editor Video Pro']
    }
    
    data = []
    start_date = datetime(2025, 1, 1)
    
    for i in range(num_rows):
        categoria = random.choice(list(products.keys()))
        producto = random.choice(products[categoria])
        
        # Precios base aproximados
        base_price = {
            'Laptop Pro 15': 1200, 'Monitor 27" 4K': 500, 'Tablet Air': 650, 'Smartphone X': 900, 'Auriculares Noise-Cancelling': 250,
            'Ratón Ergonómico': 60, 'Teclado Mecánico': 120, 'Webcam HD': 80, 'Cable HDMI 2.1': 25, 'Hub USB-C': 45,
            'Silla Ergonómica': 300, 'Escritorio Elevable': 450, 'Lámpara LED': 35, 'Soporte Monitor': 70,
            'Licencia Office': 150, 'Antivirus Personal': 40, 'Suscripción Cloud': 120, 'Editor Video Pro': 300
        }
        
        price = base_price[producto] * (1 + random.uniform(-0.1, 0.2))
        cost = price * random.uniform(0.4, 0.7)
        
        fecha = start_date + timedelta(days=random.randint(0, 450))
        
        data.append({
            'Fecha': fecha.strftime('%Y-%m-%d'),
            'Producto': producto,
            'Categoria': categoria,
            'Ventas_EUR': round(price, 2),
            'Coste_EUR': round(cost, 2)
        })
        
    df = pd.DataFrame(data)
    # Ordenar por fecha
    df = df.sort_values(by='Fecha')
    output_path = r'c:\Users\christianjimenezdiaz\OneDrive - decide\Documentos\New project\data\ventas_grandes_test.csv'
    df.to_csv(output_path, index=False)
    print(f"Generated {num_rows} rows at {output_path}")

if __name__ == "__main__":
    generate_sales_data(5000)
