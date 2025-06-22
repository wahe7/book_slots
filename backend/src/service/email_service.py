import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from src.config.email_config import email_settings

class EmailService:
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send an email using SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            text_content: Plain text content of the email (optional)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not text_content:
            # Simple conversion from HTML to plain text if text_content not provided
            import re
            text_content = re.sub(r'<[^>]*>', '', html_content)
            
        # Create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{email_settings.EMAIL_FROM_NAME} <{email_settings.EMAIL_FROM}>"
        msg['To'] = to_email
        
        # Attach parts
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        try:
            # Create secure connection and send email
            with smtplib.SMTP(email_settings.SMTP_SERVER, email_settings.SMTP_PORT) as server:
                server.starttls()
                
                # Login if credentials are provided
                if email_settings.SMTP_USERNAME and email_settings.SMTP_PASSWORD:
                    server.login(email_settings.SMTP_USERNAME, email_settings.SMTP_PASSWORD)
                
                # Send the email
                server.send_message(msg)
                return True
                
        except smtplib.SMTPException:
            return False
        except Exception:
            return False
    
    @staticmethod
    def send_booking_confirmation(
        to_email: str,
        name: str,
        event_name: str,
        slot_time: str,
        booking_id: int
    ) -> bool:
        """
        Send a booking confirmation email
        
        Args:
            to_email: Recipient email address
            name: Name of the person who made the booking
            event_name: Name of the event
            slot_time: Time of the booked slot
            booking_id: ID of the booking
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        subject = f"Booking Confirmation - {event_name}"
        
        html_content = f"""
        <html>
            <body>
                <h2>Booking Confirmation</h2>
                <p>Dear {name},</p>
                <p>Your booking has been confirmed with the following details:</p>
                <ul>
                    <li><strong>Event:</strong> {event_name}</li>
                    <li><strong>Time Slot:</strong> {slot_time}</li>
                    <li><strong>Booking ID:</strong> {booking_id}</li>
                </ul>
                <p>Thank you for using our service!</p>
                <p>Best regards,<br>The BookSlot Team</p>
            </body>
        </html>
        """
        
        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )
