from pydantic import BaseModel, Field


class Metadata(BaseModel):
    sender: str = Field(description="The sender of the email")
    subject: str = Field(description="The subject of the email")
    date: str = Field(description="The date of the email")
    to: list[str] = Field(description="The recipients of the email")
    cc: list[str] = Field(description="The carbon copy recipients of the email")

class LinkEvaluation(BaseModel):
    link: str = Field(description="The link of the email")
    origin: str = Field(description="The origin of the link. 0-30 → Highly Suspicious, 31-60 → Uncertain / Mixed Signals, 61-100 → Likely Legitimate")
    evalution: str = Field(description="The evaluation of the link. 0-30 → Highly Suspicious, 31-60 → Uncertain / Mixed Signals, 61-100 → Likely Legitimate")
    reason: str = Field(description="The reason for the evaluation")

class AttachmentEvaluation(BaseModel):
    link: str = Field(description="The Attachment of the email")
    evalution: str = Field(description="The evaluation of the Attachment. 0-30 → Highly Suspicious, 31-60 → Uncertain / Mixed Signals, 61-100 → Likely Legitimate")
    reason: str = Field(description= "The reason for the evaluation")

class EmailReport(BaseModel):
    credibility_percentage: str = Field(description="The credibility percentage of the email.0-30 → Highly Suspicious, 31-60 → Uncertain / Mixed Signals, 61-100 → Likely Legitimate")
    red_flags: list[str] = Field(description="The red flags of the email")
    green_flags: list[str] = Field(description="The green flags of the email")
    metadata: Metadata = Field(description="The metadata of the email")
    links: list[LinkEvaluation] = Field(description="The links of the email")
    attachments: list[AttachmentEvaluation] = Field(description="The attachments of the email")
    intent: list[str] = Field(description="The intent classification labels for the email, e.g., phishing, scam, spam, legitimate.")
    recommended_action: str = Field(description="The recommended action: allow, flag_for_review, block, or quarantine.")