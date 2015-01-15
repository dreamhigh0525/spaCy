=======
License
=======

I've been writing spaCy for six months now, and I'm very excited to release it.
I think it's the most valuable thing I could have built.  When I was in
academia, I noticed that small companies couldn't really make use of our work.
Meanwhile the tech giants have been hiring *everyone*, and putting this stuff
into production.  I think spaCy can change that.  


  +------------+-----------+----------+-------------------------------------+
  | License    | Price     | Term     | Suitable for                        |
  +============+===========+==========+=====================================+
  | Commercial | $5,000    | Life     | Production use                      |
  +------------+-----------+----------+-------------------------------------+
  | Trial      | $1        | 90 days  | Evaluation, seed startup            |
  +------------+-----------+----------+-------------------------------------+
  | AGPLv3     | Free      | Life     | Research, teaching, hobbyists, FOSS |
  +------------+-----------+----------+-------------------------------------+

To make spaCy as valuable as possible, licenses to it are for life.  You get
complete transparency, certainty and control.  There is much less risk this
way.  And if you're ever in acquisition or IPO talks, the story is simple.

spaCy can also be used as free open-source software, under the Aferro GPL
license.  If you use it this way, you must comply with the AGPL license terms.
When you distribute your project, or offer it as a network service, you must
distribute the source-code, and grant users an AGPL license to it.


.. I left academia in June 2014, just when I should have been submitting my first
  grant proposal.  Grant writing seemed a bad business model.  I wasn't sure
  exactly what I would do instead, but I knew that the work I could do was
  valuable, and that it would make sense for people to pay me to do it, and that
  it's often easy to convince smart people of things that are true.

.. I left because I don't like the grant system.  It's not the
  best way to create value, and it's not the best way to get paid.


Examples
--------

In order to clarify how spaCy's license structure might apply to you, I've
written a few examples, in the form of user-stories.  

Ashley and Casey: Seed stage start-up
#####################################

Ashley and Casey have an idea for a start-up.  To explore their idea, they want
to build a minimum viable product they can put in front of potential users and
investors. 

They have two options.

  1. **Trial commercial license.** With a simple form, they can use spaCy for 90
    days, for a nominal fee of $1.  They are free to modify spaCy, and they
    will own the copyright to their modifications for the duration of the license.
    After the trial period elapses, they can either pay the license fee, stop
    using spaCy, release their project under the AGPL.

  2. **AGPL.**  Casey and Pat can instead use spaCy under the AGPL license.
     However, they must then release any code that statically or dynamically
     links to spaCy under the AGPL as well (e.g. if they import the module, or
     import a module that imports it, etc).  They also cannot use spaCy as
     a network resource, by running it as a service --- this is the
     loophole that the "A" part of the AGPL is designed to close.
     
Ashley and Casey find the AGPL license unattractive for commercial use.
They decide to take up the trial commercial license.
However,  over the next 90 days, Ashley has to move house twice, and Casey gets
sick.  By the time the trial expires, they still don't have a demo they can show
investors.  They send an email explaining the situation, and a 90 day extension
to their trial license is granted.

By the time the extension period has elapsed, spaCy has helped them secure
funding, and they even have a little revenue.  They are glad to pay the $5,000
commercial license fee.

spaCy is now permanently licensed for the product Ashley and Casey are
developing.  They own the copyright to any modifications they make to spaCy,
but not to the original spaCy code.

No additional fees will be due when they hire new developers, run spaCy on
additional internal servers, etc. If their company is acquired, the license will
be transferred to the company acquiring them.  However, to use spaCy in another
product, they will have to buy a second license.


Alex and Sasha: University Academics
####################################

Alex and Sasha are post-doctoral researchers working for a university.  Part of
their funding comes from a grant from Google, but Google will not own any part
of the work that they produce.  Their mission is just to write papers.

Alex and Sasha find spaCy convenient, so they use it in their system under the
AGPL.  This means that their system must also be released under the AGPL, but they're
cool with that --- they were going to release their code anyway, as it's the only
way to ensure their experiments are properly repeatable.

Alex and Sasha find and fix a few bugs in spaCy.  They must release these
modifications, and they ask that they be accepted into the main spaCy repo.
In order to do this, they must sign a contributor agreement, ceding their
copyright.  When commercial licenses to spaCy are sold, Alex and Sasha will
not be able to claim any royalties from their contributions.

Later, Alex and Sasha implement new features into spaCy, for another paper. The
code was quite rushed, and they don't want to take the time to put together a
proper pull request. They must release their modifications under the AGPL, but
they are not obliged to contribute it to the spaCy repository, or concede their
copyright.


Phuong and Jessie: Open Source developers
#########################################

Phuong and Jessie use the Calibre to manage their e-book libraries. They have an
idea for a search feature, and they want to use spaCy to implement it. Calibre is
released under the GPLv3. The AGPL has additional restrictions for projects
used as a network resource, but they don't apply to this project, so Phuong and
Jessie can use spaCy to improve Calibre.  They'll have to release their code, but
that was always their intention anyway.
