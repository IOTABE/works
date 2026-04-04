from accounts.models import CustomUser, ClientProfile, ProfessionalProfile
from services.models import Category, ServiceOffer, ServiceRequest

# Clean DB if running multiple times
Category.objects.all().delete()
CustomUser.objects.all().delete()

# Create users
u1 = CustomUser.objects.create_user(username='joao', password='123', email='joao@test.com')
u2 = CustomUser.objects.create_user(username='maria', password='123', email='maria@test.com')

# Create profiles
p1 = ClientProfile.objects.create(user=u1, phone='11 99999-9999')
p2 = ProfessionalProfile.objects.create(user=u2, phone='11 88888-8888', bio='Especialista em manutenção da casa.')

# Create categories
cat1 = Category.objects.create(name='Serviços Gerais', slug='servicos-gerais')
cat2 = Category.objects.create(name='Aulas Particulares', slug='aulas')

# Create Offers
ServiceOffer.objects.create(
    professional=p2,
    category=cat1,
    title='Consertos de encanamento e elétrica',
    description='Atendo em toda região central para serviços diversos de reparos.',
    price_base=120.00
)

ServiceOffer.objects.create(
    professional=p2,
    category=cat2,
    title='Aulas de Violão Iniciante',
    description='Metodologia prática e direta. Aula uma vez na semana.',
    price_base=80.00
)

# Create Requests
ServiceRequest.objects.create(
    client=p1,
    category=cat1,
    title='Preciso instalar 3 ventiladores de teto urgentemente',
    description='Minha sala e 2 quartos precisam da instalação dos ventiladores. Material comprado.',
)

print("Dados de exemplo inseridos com sucesso!")
