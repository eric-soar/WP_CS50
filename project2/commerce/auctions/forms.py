from django import forms
class CreateListingForm(forms.Form):
    name = forms.CharField(label="Name")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    price = forms.CharField(label="Price")
    image = forms.ImageField(label="Image")

    def clean_price(self):
        try:
            price = float(self.cleaned_data['price'])
            if price <= 0:
                raise forms.ValidationError("Price must be greater than 0.")
            return price
        except ValueError:
            raise forms.ValidationError("Enter a valid number for the price.")

class CreateCommentForm(forms.Form):
    text = forms.CharField(label="Comment", widget=forms.Textarea)