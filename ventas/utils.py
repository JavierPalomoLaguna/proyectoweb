import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from datetime import datetime

def generar_factura_pdf(pedido):
    """Genera un PDF de factura para un pedido"""
    
    # Crear buffer para el PDF
    buffer = BytesIO()
    
    # Crear documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Centrado
    )
    
    estilo_normal = styles['Normal']
    
    # Contenido del PDF
    story = []
    
    # Título con número de factura
    story.append(Paragraph(f"FACTURA Nº {pedido.id}", estilo_titulo))
    story.append(Spacer(1, 10))
    
    # Información de LA TRASTIENDA S.L. - CORREGIDO CON CAMPOS REALES
    info_empresa = [
        ["EMITIDO POR:", "CLIENTE:"],
        ["LA TRASTIENDA S.L.", f"{pedido.cliente.nombre} {pedido.cliente.apellidos}"],
        ["Avenida de Asturias 14, 28000 Madrid", f"{pedido.cliente.calle} {pedido.cliente.numero_calle}"],
        ["CIF: B00000000", f"Portal: {pedido.cliente.portal}" if pedido.cliente.portal else ""],
        ["Teléfono: 666666666", f"Escalera: {pedido.cliente.escalera}" if pedido.cliente.escalera else ""],
        ["Email: contabilidad@latrastienda.es", f"Piso: {pedido.cliente.piso}, Puerta: {pedido.cliente.puerta}"],
        ["", f"{pedido.cliente.localidad}, {pedido.cliente.provincia}"],
        ["", f"Código Postal: {pedido.cliente.codigo_postal}"],
        ["", f"Teléfono: {pedido.cliente.telefono or 'No proporcionado'}"],
        ["", f"Email: {pedido.cliente.email}"],
        ["", f"CIF: {pedido.cliente.cif or 'No proporcionado'}"],
    ]
    
    tabla_info = Table(info_empresa, colWidths=[doc.width/2.0]*2)
    tabla_info.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    
    story.append(tabla_info)
    story.append(Spacer(1, 20))
    
    # Detalles de la factura
    detalles_factura = [
        ["Nº Factura:", f"{pedido.id}"],
        ["Fecha de emisión:", pedido.fecha.strftime("%d/%m/%Y")],
        ["Fecha de pago:", pedido.fecha_pago.strftime("%d/%m/%Y") if pedido.fecha_pago else "Pendiente"],
        ["Método de pago:", pedido.get_metodo_pago_display()],
    ]
    
    tabla_detalles = Table(detalles_factura, colWidths=[doc.width/3.0]*2)
    tabla_detalles.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    
    story.append(tabla_detalles)
    story.append(Spacer(1, 20))
    
    # Productos
    encabezados = ['Producto', 'Cantidad', 'Precio Unitario', 'Total']
    datos_productos = [encabezados]
    
    # Calcular totales
    base_imponible = 0
    iva_total = 0
    
    for linea in pedido.lineapedido_set.all():
        precio_sin_iva = float(linea.producto.precio_sin_iva)
        iva_producto = (float(linea.producto.precio_total) - precio_sin_iva) * linea.cantidad
        total_linea = float(linea.subtotal)
        
        datos_productos.append([
            linea.producto.nombre,
            str(linea.cantidad),
            f"{linea.producto.precio_total:.2f} €",
            f"{total_linea:.2f} €"
        ])
        
        base_imponible += precio_sin_iva * linea.cantidad
        iva_total += iva_producto
    
    # Gastos de envío
    if pedido.gastos_envio > 0:
        gastos_envio_float = float(pedido.gastos_envio)
        iva_envio = gastos_envio_float * 0.21  # 21% IVA envío
        base_imponible_envio = gastos_envio_float - iva_envio
        
        datos_productos.append([
            "Gastos de envío",
            "1",
            f"{pedido.gastos_envio:.2f} €",
            f"{pedido.gastos_envio:.2f} €"
        ])
        
        base_imponible += base_imponible_envio
        iva_total += iva_envio
    elif pedido.envio_gratis:
        datos_productos.append([
            "Gastos de envío (Gratis)",
            "1",
            "0.00 €",
            "0.00 €"
        ])
    
    # Tabla de productos
    tabla_productos = Table(datos_productos, colWidths=[doc.width*0.5, doc.width*0.15, doc.width*0.15, doc.width*0.2])
    tabla_productos.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,1), (-1,-1), 9),
    ]))
    
    story.append(tabla_productos)
    story.append(Spacer(1, 20))
    
    # Totales
    totales = [
        ["BASE IMPONIBLE:", f"{base_imponible:.2f} €"],
        ["IVA (21%):", f"{iva_total:.2f} €"],
        ["TOTAL:", f"{pedido.total:.2f} €"],
    ]
    
    tabla_totales = Table(totales, colWidths=[doc.width*0.7, doc.width*0.3])
    tabla_totales.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('LINEABOVE', (0,2), (-1,2), 1, colors.black),
    ]))
    
    story.append(tabla_totales)
    
    # Pie de página
    story.append(Spacer(1, 30))
    story.append(Paragraph("Gracias por su compra - LA TRASTIENDA S.L.", styles['Normal']))
    
    # Generar PDF
    doc.build(story)
    
    # Obtener contenido del PDF
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf