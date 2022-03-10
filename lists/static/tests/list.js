let initialize = ()=> {
  $('input[name="text"]').on('keypress', ()=> {
    $('.has-error').hide();
  });
};