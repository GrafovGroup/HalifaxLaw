const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('#navigation');
menu?.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); nav.classList.toggle('open', open); });
document.addEventListener('keydown', e => { if(e.key === 'Escape' && nav?.classList.contains('open')) { nav.classList.remove('open'); menu.setAttribute('aria-expanded','false'); menu.focus(); } });
const search = document.querySelector('#community-search');
if(search) { const cards = [...document.querySelectorAll('[data-search]')]; const fr = document.documentElement.lang.startsWith('fr'); const normalize = s => s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9 ]/g,''); search.addEventListener('input',()=> { const q=normalize(search.value); let n=0; cards.forEach(c=>{ c.hidden=!normalize(c.dataset.search).includes(q); if(!c.hidden)n++; }); document.querySelector('#search-status').textContent = n ? (fr ? `${n} guide(s) correspondant(s).` : `${n} matching guide${n===1?'':'s'}.`) : (fr ? 'Aucun guide correspondant. Essayez une collectivité voisine.' : 'No matching guides. Try a nearby community.'); }); }

// Native POST remains available when JavaScript is unavailable.
const enquiry = document.querySelector('#enquiry-form');
if (enquiry && window.fetch && window.FormData && window.AbortController) {
  const topicMap = {'property':'Real estate','family':'Family','wills-estates':'Estates','business':'Business','housing':'Tenancies','disputes':'Disputes','criminal-law':'Criminal law'};
  const selectedTopic = new URLSearchParams(window.location.search).get('topic');
  if (topicMap[selectedTopic]) {
    enquiry.elements.topic.value = topicMap[selectedTopic];
    document.querySelectorAll('a.language').forEach(link => { link.href += '?topic=' + encodeURIComponent(selectedTopic) + '#enquiry'; });
  }
  const fr = document.documentElement.lang.startsWith('fr');
  const copy = (en, french) => fr ? french : en;
  const status = enquiry.querySelector('#form-status');
  const fields = [...enquiry.querySelectorAll('fieldset input, fieldset select, fieldset textarea')];
  const group = enquiry.querySelector('fieldset');
  const submit = enquiry.querySelector('button[type=submit]');
  const label = submit.textContent;
  let busy = false;
  enquiry.noValidate = true;
  const clear = field => {
    field.removeAttribute('aria-invalid');
    document.getElementById(`error-${field.name}`).textContent = '';
  };
  const invalid = (field, message) => {
    field.setAttribute('aria-invalid', 'true');
    document.getElementById(`error-${field.name}`).textContent = message;
  };
  fields.forEach(field => field.addEventListener('input', () => clear(field)));
  enquiry.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
    fields.forEach(clear);
    status.textContent = '';
    const errors = fields.filter(field => !field.validity.valid);
    if (errors.length) {
      errors.forEach(field => invalid(field, field.validity.typeMismatch ? copy('Enter a valid email address.', 'Saisissez une adresse courriel valide.') : copy('Please complete this field.', 'Veuillez remplir ce champ.')));
      status.textContent = copy('Please check the highlighted fields.', 'Veuillez vérifier les champs indiqués.');
      errors[0].focus();
      return;
    }
    if (enquiry.elements._gotcha.value) return;
    const body = new FormData(enquiry);
    busy = true;
    group.disabled = true;
    enquiry.setAttribute('aria-busy', 'true');
    submit.textContent = copy('SENDING…', 'ENVOI…');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    let accepted = false;
    try {
      const response = await fetch(enquiry.action, {method: 'POST', body, headers: {'Accept': 'application/json'}, signal: controller.signal});
      const data = await response.json();
      if (response.ok && data.ok === true) {
        accepted = true;
        enquiry.reset();
        group.hidden = true;
        status.textContent = copy('Thank you. Your enquiry has been accepted for delivery. The practice will need to confirm whether it can assist. For a time-sensitive matter, call (289) 888-5878.', 'Merci. Votre demande a été acceptée pour acheminement. Le cabinet devra confirmer s’il peut vous aider. Pour une question urgente, appelez le (289) 888-5878.');
      } else {
        for (const error of data.errors || []) {
          const field = fields.find(field => field.name === error.field);
          if (field) invalid(field, copy('Please check this entry.', 'Veuillez vérifier cette réponse.'));
        }
        status.textContent = copy('Your enquiry was not accepted. Please check your entries and try again, or contact info@halifaxlaw.ca / (289) 888-5878.', 'Votre demande n’a pas été acceptée. Vérifiez vos réponses et réessayez, ou contactez info@halifaxlaw.ca / (289) 888-5878.');
      }
    } catch {
      status.textContent = copy('We could not confirm submission. Your entries are still here. Please contact info@halifaxlaw.ca / (289) 888-5878 before resending to avoid a duplicate enquiry.', 'Nous n’avons pas pu confirmer l’envoi. Vos réponses sont conservées sur cette page. Contactez info@halifaxlaw.ca / (289) 888-5878 avant de renvoyer pour éviter un doublon.');
    } finally {
      clearTimeout(timeout);
      enquiry.removeAttribute('aria-busy');
      if (!accepted) { busy = false; group.disabled = false; }
      submit.textContent = label;
      status.focus();
    }
  });
}

// Close the mobile menu when focus leaves it or a link is followed.
const closeMenu = () => { nav?.classList.remove('open'); menu?.setAttribute('aria-expanded', 'false'); };
nav?.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('click', event => { if (!event.target.closest('header')) closeMenu(); });
document.querySelector('header')?.addEventListener('focusout', event => { if (!event.currentTarget.contains(event.relatedTarget)) closeMenu(); });
window.matchMedia('(min-width: 801px)').addEventListener('change', closeMenu);
