
from flask import Flask, render_template, request, redirect, url_for
from oppslag import Oppslag
from oppslag_reg import OppslagReg
from update_form import UpdateForm
from new_form import NewForm

app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])


def oppslag() -> 'html':

    id = request.args.get('id')
    kategori = request.args.get('kategori')

    if kategori:
        if kategori == "hjem":  # Hjem -> viser alle
            with OppslagReg() as db:
                result = db.show_all()
            alle_oppslag = [Oppslag(*x) for x in result]
            return render_template(
                'alle_oppslag.html',
                alle_oppslag=alle_oppslag)

        else:
            with OppslagReg() as db:
                result = db.show_kategori(kategori)
            kategori = [Oppslag(*x) for x in result]
            return render_template('kategori.html', kategori=kategori)

    elif id:
        with OppslagReg() as db:
            db.count_treff(id)
            oppslag = Oppslag(*db.show_oppslag(id))
        return render_template('oppslag.html', oppslag=oppslag)

    else:
        with OppslagReg() as db:
            result = db.show_all()
        alle_oppslag = [Oppslag(*x) for x in result]
        return render_template(
            'alle_oppslag.html',
            alle_oppslag=alle_oppslag)

@app.route('/nytt_oppslag', methods=["GET", "POST"])

def new_oppslag() -> 'html':
    form = NewForm(request.form)

    if request.method == "POST" and form.validate():
        tittel = form.tittel.data
        ingress = form.ingress.data
        oppslagstekst = form.oppslagstekst.data
        kategori = form.kategori.data
        bruker = request.bruker.data

        oppslag = (tittel, ingress, oppslagstekst, kategori, bruker)

        with OppslagReg() as db:
            db.new_oppslag(oppslag)
        return redirect(url_for('oppslag'))
    else:
        return render_template('nytt_oppslag.html', form=form)

@app.route('/update', methods=["GET", "POST"])

def update() -> 'html':
    id = request.args.get('id')

    with OppslagReg() as db:
        oppslag = Oppslag(*db.show_oppslag(id))

    # Fyller inn info i form
    form = UpdateForm(obj=oppslag)
    form.populate_obj(oppslag)

    if request.method == "POST" and form.validate():
        id = request.form['id']
        tittel = form.tittel.data
        ingress = form.ingress.data
        oppslagstekst = form.oppslagstekst.data
        kategori = form.kategori.data

        oppslag = (tittel, ingress, oppslagstekst, kategori, id)

        with OppslagReg() as db:
            db.update_oppslag(oppslag)
        return redirect(url_for('oppslag'))
    else:
        return render_template('update_oppslag.html', form=form)


@app.route('/delete_confirm')

# Kode hentet fra forelesning
def delete_confirm() -> 'html':
    id = request.args.get('id')
    if not id:
        return render_template('error.html',
                               msg='Invalid parameter')
    else:
        with OppslagReg() as db:
            opps = db.show_oppslag(id)
            if opps is None:
                return render_template('error.html',
                                       msg='Invalid parameter')
            else:
                oppslag = Oppslag(*opps)
                return render_template(
                    'delete_oppslag.html',
                    oppslag=oppslag, deleteConfirmation=True)


@app.route('/delete', methods=["GET", "POST"])

# Kode hentet fra forelesning
def delete() -> 'html':
    if request.method == "POST":
        id = request.form['id']

        with OppslagReg() as db:
            db.delete_oppslag(id)

        return redirect(url_for('oppslag'))


if __name__ == "__main__":
    app.run(debug=True)
