from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(order):
    subject = f"Grocera Order Confirmation"
    message = f"""
    Hi {order.user.first_name},
    Thank you for your order {order.user.first_name}!
    Order details:
    """
    for item in order.items.all():
        message += f"Product: {item.product.name}, Quantity: {item.quantity}, Price: {item.price}\n"
    message += f"\nTotal Price: {order.total_price}\n\nWe will notify you once your order ships.\n\nBest regards,\nGrocera"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.user.email],
        fail_silently=False,
    )
    print(f"Sending order confirmation email to: {order.user.email}")
