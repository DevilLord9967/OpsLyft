import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

import boto3

EMAIL_ID = "ops.eregistry@dvara.com"
EMAIL_PASSWORD = "Welcome@2021"


def send_mail(
    subject: str,
    email_body: str,
    recipients: List[str],
):
    """Sends Mail

    Keyword arguments:
    subject -- Mail Subject
    email_body -- Mail Body
    recipients -- Recipients of the mail
    Return: None
    """

    sender = EMAIL_ID
    gmail_password = EMAIL_PASSWORD
    COMMASPACE = ", "

    outer = MIMEMultipart()
    outer["Subject"] = subject
    outer["To"] = COMMASPACE.join(recipients)
    outer["From"] = sender
    outer.preamble = "You will not see this in a MIME-aware mail reader.\n"

    body = MIMEText(email_body, "plain")
    outer.attach(body)
    composed = outer.as_string()

    # Send the email
    with smtplib.SMTP("smtp.office365.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(sender, gmail_password)
        s.sendmail(sender, recipients, composed)
        s.close()


DEFAULT_MAIL = "deepaksinghal9967@gmail.com"


class EC2(object):
    def __init__(self, region: str, mandatory_tags: List[str]) -> None:
        self.region = region
        self.instances = boto3.resource("ec2", self.region).instances.filter(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )
        self.mandatory_tags = mandatory_tags
        self.instancesids_to_stop = []

    def check_valid_instances(self) -> List[str]:
        for instance in self.instances:
            invalid_tags = self.mandatory_tags
            user = DEFAULT_MAIL
            mail_sent = False
            # print(instance.id)
            # print(instance.tags)
            if instance.tags is not None:
                for tag in instance.tags:
                    if tag["Key"] == "created by":
                        user = tag["Value"]
                    elif tag["Key"] == "sent_mail":
                        mail_sent = True
                        mail_send_time = datetime.strptime(
                            tag["Value"], "%Y-%m-%d %H:%M:%S"
                        )
                    elif tag["Key"] in invalid_tags:
                        invalid_tags.remove(tag["Key"])
                    if invalid_tags == []:
                        break
            else:
                print(f"No tags present for instance :{instance.id}")

            if not mail_sent and invalid_tags != []:
                mail_body = """
                The instance created having ID: {} is not following the given criteria, please the find the list of missing tags below:
                {}
                """.format(
                    instance.id, "                 >".join(invalid_tags)
                )
                send_mail(
                    subject="Invalid Instance created",
                    email_body=mail_body,
                    recipients=[user],
                )

                # create Tag
                # tag = [{'Key':'sent_mail', 'Value':str(datetime.now())[:-7]}]

                instance.create_tags(
                    Tags=[{"Key": "sent_mail", "Value": str(datetime.now())[:-7]}]
                )
            if mail_sent:
                print((datetime.now() - mail_send_time))
            if mail_sent and (datetime.now() - mail_send_time) >= timedelta(minutes=2):
                mail_body = """
                The instance created having ID: {}, due to not following the give criteria is stopped.
                """.format(
                    instance.id
                )
                send_mail(
                    subject="Invalid Instance Stopped",
                    email_body=mail_body,
                    recipients=[user],
                )
                instance.delete_tags(Tags=[{"Key": "sent_mail"}])
                self.instancesids_to_stop.append(instance.id)

    def stop_invalid_instances(self):
        ec2_client = boto3.client("ec2", region_name=self.region)
        ec2_client.stop_instances(InstanceIds=self.instancesids_to_stop)


def lambda_handler(event, context):
    ec2 = EC2(region="ap-south-1", mandatory_tags=["Environment", "Name"])
    ec2.check_valid_instances()
    ec2.stop_invalid_instances()


if __name__ == "__main__":
    lambda_handler(None, None)
