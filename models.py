from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.timezone import datetime

# Create your models here.


class ChiefEditor (models.Model):
    editor_id = models.AutoField(primary_key=True)
    ename = models.CharField(max_length=25)

    def __unicode__(self):
        return self.editor_id, self.ename

    def __str__(self):
        return str(self.editor_id) + " | " + str(self.ename)


class Author (models.Model):
    authorid = models.AutoField(primary_key=True)
    aname = models.CharField(max_length=20)

    def __unicode__(self):
        return self.authorid, self.aname

    def __str__(self):
        return str(self.authorid) + " | " + str(self.aname)


class Publisher(models.Model):
    publisherid = models.AutoField(primary_key=True)
    pubname = models.CharField(max_length=25)
    address = models.TextField(max_length=50)

    def __unicode__(self):
        return self.publisherid, self.pubname

    def __str__(self):
        return str(self.publisherid) + " | " + str(self.pubname)


class Branch(models.Model):
    libid = models.AutoField(primary_key=True)
    lname = models.CharField(max_length=30)
    llocation = models.CharField(max_length=50)

    def __unicode__(self):
        return self.libid, self.lname

    def __str__(self):
        return str(self.libid) + " | " + str(self.lname)


class Document(models.Model):
    docid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    pdate = models.DateField()
    publisherid = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.docid, self.title

    def __str__(self):
        return str(self.docid) + " | " + str(self.title)


class Book (models.Model):
    book_id = models.AutoField(primary_key=True)
    docid = models.OneToOneField(Document, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, validators=[RegexValidator(r'^(\d{13})$')])

    def __unicode__(self):
        return self.docid, self.isbn

    def __str__(self):
        return str(self.docid) + " | " + str(self.isbn)


class Proceedings(models.Model):
    proceedings_id = models.AutoField(primary_key=True)
    docid = models.OneToOneField(Document, on_delete=models.CASCADE)
    cdate = models.DateField()
    clocation = models.CharField(max_length=50)
    ceditor = models.CharField(max_length=20)

    def __unicode__(self):
        return self.docid, self.ceditor

    def __str__(self):
        return str(self.docid) + " | " + str(self.ceditor)


class JournalVolume (models.Model):
    jvolume_id = models.AutoField(primary_key=True)
    docid = models.ForeignKey(Document, on_delete=models.CASCADE)
    jvolume = models.IntegerField()
    editor_id = models.ForeignKey(ChiefEditor, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.docid, self.jvolume

    def __str__(self):
        return str(self.docid) + " | " + str(self.jvolume)


class JournalIssue (models.Model):
    jissue_id = models.AutoField(primary_key=True)
    docid = models.ForeignKey(JournalVolume, on_delete=models.CASCADE)
    issue_no = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    scope = models.CharField(max_length=50)

    class Meta:
        unique_together = (("docid", "issue_no"),)

    def __unicode__(self):
        return self.docid, self.issue_no

    def __str__(self):
        return str(self.docid) + " | " + str(self.issue_no)


class Writes(models.Model):
    docid = models.ForeignKey(Document, on_delete=models.CASCADE)
    authorid = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("docid", "authorid"),)

    def __unicode__(self):
        return self.docid, self.authorid

    def __str__(self):
        return str(self.docid) + " | " + str(self.authorid)


class InvEditor(models.Model):
    issue_id = models.ForeignKey(JournalIssue, on_delete=models.CASCADE)
    iename = models.CharField(max_length=30)

    class Meta:
        unique_together = (("issue_id", "iename"),)

    def __unicode__(self):
        return self.issue_id, self.iename

    def __str__(self):
        return str(self.issue_id) + " | " + str(self.iename)


class Copy(models.Model):
    copyid = models.AutoField(primary_key=True)
    docid = models.ForeignKey(Document, on_delete=models.CASCADE)
    copyno = models.IntegerField()
    libid = models.ForeignKey(Branch, on_delete=models.CASCADE)
    position = models.CharField(max_length=6, validators=[
        RegexValidator(
            regex='^[0-9]{3}[A-Z][0-9]{2}',
            message='Copy Position Should be like 001A03',
            code='invalid_position'
        ),
    ])
    status = models.BooleanField(default=True)

    class Meta:
        unique_together = (("docid", "copyno", "libid"),)

    def __unicode__(self):
        return self.docid, self.copyno

    def __str__(self):
        return str(self.libid) + " | " + str(self.docid) + " | " + str(self.copyno)


class Reader(models.Model):
    Reader_type = (("Student", "Student"), ("Senior Citizen", "Senior Citizen"), ("Staff", "Staff"),
                   ("Others", "Others"))
    readerid = models.AutoField(primary_key=True)
    rtype = models.CharField(max_length=15, choices=Reader_type)
    rname = models.CharField(max_length=25)
    address = models.TextField(max_length=50)

    def __unicode__(self):
        return self.readerid, self.rname

    def __str__(self):
        return str(self.readerid) + " | " + str(self.rname)


class Borrows(models.Model):
    bornumber = models.AutoField(primary_key=True)
    readerid = models.ForeignKey(Reader, on_delete=models.CASCADE)
    copyid = models.ForeignKey(Copy, on_delete=models.CASCADE)
    bdtime = models.DateTimeField(default=datetime.now, blank=True)
    rdtime = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.readerid, self.bornumber

    def __str__(self):
        return str(self.bornumber) + " | " + str(self.readerid) + " | " + str(self.copyid)


class Reserves(models.Model):
    resnumber = models.AutoField(primary_key=True)
    readerid = models.ForeignKey(Reader, on_delete=models.CASCADE)
    copyid = models.ForeignKey(Copy, on_delete=models.CASCADE)
    dtime = models.DateTimeField(default=datetime.now, blank=True)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.readerid, self.resnumber

    def __str__(self):
        return str(self.resnumber) + " | " + str(self.readerid) + " | " + str(self.copyid)


class Fine(models.Model):
    fine_id = models.AutoField(primary_key=True)
    fine = models.FloatField()
    bornum = models.OneToOneField(Borrows,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fine_id) + " | " + str(self.fine) + " | " + str(self.bornum)
