import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path

from image_processor import process_images, add_watermark
from customer_manager import import_customers, export_customers, search_customers
from order_tracker import init_db, add_order, list_orders, update_order_status

app = typer.Typer(help="Local CLI tool for e-commerce merchants")
console = Console()

@app.command()
def process_product_images(
    input_dir: Path = typer.Argument(..., help="Directory containing product images"),
    output_dir: Path = typer.Argument(..., help="Output directory for processed images"),
    width: int = typer.Option(800, help="Target width in pixels"),
    height: int = typer.Option(800, help="Target height in pixels"),
    watermark_text: str = typer.Option(None, help="Watermark text to add"),
):
    """Batch process product images: resize and add watermark"""
    console.print(f"[cyan]Processing images from {input_dir}...[/cyan]")
    processed = process_images(input_dir, output_dir, width, height)
    
    if watermark_text:
        console.print(f"[cyan]Adding watermark: {watermark_text}[/cyan]")
        add_watermark(output_dir, watermark_text)
    
    console.print(f"[green]✓ Processed {processed} images[/green]")

@app.command()
def import_customer_data(
    csv_file: Path = typer.Argument(..., help="CSV file to import"),
    db_file: Path = typer.Option("customers.csv", help="Customer database file"),
):
    """Import customers from CSV file"""
    count = import_customers(csv_file, db_file)
    console.print(f"[green]✓ Imported {count} customers[/green]")

@app.command()
def export_customer_data(
    output_file: Path = typer.Argument(..., help="Output CSV file"),
    db_file: Path = typer.Option("customers.csv", help="Customer database file"),
):
    """Export customers to CSV file"""
    count = export_customers(db_file, output_file)
    console.print(f"[green]✓ Exported {count} customers[/green]")

@app.command()
def search_customer(
    query: str = typer.Argument(..., help="Search query (name or email)"),
    db_file: Path = typer.Option("customers.csv", help="Customer database file"),
):
    """Search customers by name or email"""
    results = search_customers(db_file, query)
    
    if results.empty:
        console.print("[yellow]No customers found[/yellow]")
        return
    
    table = Table(title="Search Results")
    for col in results.columns:
        table.add_column(col)
    
    for _, row in results.iterrows():
        table.add_row(*[str(v) for v in row])
    
    console.print(table)

@app.command()
def create_order(
    customer_name: str = typer.Option(..., help="Customer name"),
    product: str = typer.Option(..., help="Product name"),
    amount: float = typer.Option(..., help="Order amount"),
    db_file: Path = typer.Option("orders.db", help="Order database file"),
):
    """Create a new order"""
    init_db(db_file)
    order_id = add_order(db_file, customer_name, product, amount)
    console.print(f"[green]✓ Created order #{order_id}[/green]")

@app.command()
def show_orders(
    status: str = typer.Option(None, help="Filter by status (pending/shipped/completed)"),
    db_file: Path = typer.Option("orders.db", help="Order database file"),
):
    """List all orders"""
    init_db(db_file)
    orders = list_orders(db_file, status)
    
    if not orders:
        console.print("[yellow]No orders found[/yellow]")
        return
    
    table = Table(title="Orders")
    table.add_column("ID")
    table.add_column("Customer")
    table.add_column("Product")
    table.add_column("Amount")
    table.add_column("Status")
    table.add_column("Date")
    
    for order in orders:
        table.add_row(*[str(v) for v in order])
    
    console.print(table)

@app.command()
def update_order(
    order_id: int = typer.Argument(..., help="Order ID"),
    status: str = typer.Argument(..., help="New status (pending/shipped/completed)"),
    db_file: Path = typer.Option("orders.db", help="Order database file"),
):
    """Update order status"""
    init_db(db_file)
    update_order_status(db_file, order_id, status)
    console.print(f"[green]✓ Updated order #{order_id} to {status}[/green]")

if __name__ == "__main__":
    app()
