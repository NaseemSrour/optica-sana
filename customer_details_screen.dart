import 'package:flutter/material.dart';

// Data model for the Customer
class Customer {
  final int id;
  String ssn;
  String fname;
  String lname;
  String birthDate;
  String sex;
  String? telHome;
  String? telMobile;
  String? address;
  String? town;
  String? postalCode;
  String? status;
  String? org;
  String? occupation;
  String? hobbies;
  String? referer;
  String? notes;
  final int glassesNum;
  final int lensesNum;
  final bool mailing;

  Customer({
    required this.id,
    required this.ssn,
    required this.fname,
    required this.lname,
    required this.birthDate,
    required this.sex,
    this.telHome,
    this.telMobile,
    this.address,
    this.town,
    this.postalCode,
    this.status,
    this.org,
    this.occupation,
    this.hobbies,
    this.referer,
    this.notes,
    required this.glassesNum,
    required this.lensesNum,
    required this.mailing,
  });
}

// Placeholder for the CustomerService
class CustomerService {
  Future<void> updateCustomer(Customer customer) async {
    // In a real app, this would make an API call to update the customer data.
    print("Updating customer: ${customer.fname} ${customer.lname}");
    // Simulate a network delay
    await Future.delayed(const Duration(seconds: 1));
    print("Customer updated successfully.");
  }

  Future<Customer> getCustomer(int id) async {
    // In a real app, this would fetch customer data from an API or database.
    // Returning a dummy customer for demonstration purposes.
    await Future.delayed(const Duration(seconds: 1));
    return Customer(
      id: 1,
      ssn: "123456789",
      fname: "John",
      lname: "Doe",
      birthDate: "1990-01-15",
      sex: "Male",
      telHome: "555-1234",
      telMobile: "555-5678",
      address: "123 Main St",
      town: "Anytown",
      postalCode: "12345",
      status: "Active",
      org: "Some Org",
      occupation: "Software Developer",
      hobbies: "Coding, Hiking",
      referer: "Friend",
      notes: "Initial consultation.",
      glassesNum: 2,
      lensesNum: 1,
      mailing: true,
    );
  }
}

class CustomerDetailsScreen extends StatefulWidget {
  final Customer customer;
  final CustomerService customerService;

  const CustomerDetailsScreen({
    super.key,
    required this.customer,
    required this.customerService,
  });

  @override
  State<CustomerDetailsScreen> createState() => _CustomerDetailsScreenState();
}

class _CustomerDetailsScreenState extends State<CustomerDetailsScreen> {
  bool _isEditing = false;
  final _formKey = GlobalKey<FormState>();
  late final Map<String, TextEditingController> _controllers;

  @override
  void initState() {
    super.initState();
    _controllers = {
      'ssn': TextEditingController(text: widget.customer.ssn),
      'fname': TextEditingController(text: widget.customer.fname),
      'lname': TextEditingController(text: widget.customer.lname),
      'birth_date': TextEditingController(text: widget.customer.birthDate),
      'sex': TextEditingController(text: widget.customer.sex),
      'tel_home': TextEditingController(text: widget.customer.telHome),
      'tel_mobile': TextEditingController(text: widget.customer.telMobile),
      'address': TextEditingController(text: widget.customer.address),
      'town': TextEditingController(text: widget.customer.town),
      'postal_code': TextEditingController(text: widget.customer.postalCode),
      'status': TextEditingController(text: widget.customer.status),
      'org': TextEditingController(text: widget.customer.org),
      'occupation': TextEditingController(text: widget.customer.occupation),
      'hobbies': TextEditingController(text: widget.customer.hobbies),
      'referer': TextEditingController(text: widget.customer.referer),
      'notes': TextEditingController(text: widget.customer.notes),
    };
  }

  void _toggleEditMode() {
    setState(() {
      _isEditing = !_isEditing;
    });
  }

  Future<void> _saveCustomer() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      final updatedCustomer = Customer(
        id: widget.customer.id,
        ssn: _controllers['ssn']!.text,
        fname: _controllers['fname']!.text,
        lname: _controllers['lname']!.text,
        birthDate: _controllers['birth_date']!.text,
        sex: _controllers['sex']!.text,
        telHome: _controllers['tel_home']!.text,
        telMobile: _controllers['tel_mobile']!.text,
        address: _controllers['address']!.text,
        town: _controllers['town']!.text,
        postalCode: _controllers['postal_code']!.text,
        status: _controllers['status']!.text,
        org: _controllers['org']!.text,
        occupation: _controllers['occupation']!.text,
        hobbies: _controllers['hobbies']!.text,
        referer: _controllers['referer']!.text,
        notes: _controllers['notes']!.text,
        glassesNum: widget.customer.glassesNum,
        lensesNum: widget.customer.lensesNum,
        mailing: widget.customer.mailing,
      );

      try {
        await widget.customerService.updateCustomer(updatedCustomer);
        _toggleEditMode();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Customer saved successfully!')),
        );
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error saving customer: $e')),
        );
      }
    }
  }

  @override
  void dispose() {
    _controllers.forEach((_, controller) => controller.dispose());
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Customer Details${_isEditing ? " (Editing)" : ""}'),
        actions: [
          IconButton(
            icon: Icon(_isEditing ? Icons.save : Icons.edit),
            onPressed: _isEditing ? _saveCustomer : _toggleEditMode,
          ),
        ],
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16.0),
          children: _buildFormFields(),
        ),
      ),
    );
  }

  List<Widget> _buildFormFields() {
    final fields = {
      "SSN": "ssn",
      "First Name": "fname",
      "Last Name": "lname",
      "Birth Date": "birth_date",
      "Sex": "sex",
      "Home Phone": "tel_home",
      "Mobile Phone": "tel_mobile",
      "Address": "address",
      "Town": "town",
      "Postal Code": "postal_code",
      "Status": "status",
      "Organization": "org",
      "Occupation": "occupation",
      "Hobbies": "hobbies",
      "Referer": "referer",
      "Notes": "notes",
    };

    return fields.entries.map((entry) {
      return Padding(
        padding: const EdgeInsets.only(bottom: 16.0),
        child: TextFormField(
          controller: _controllers[entry.value],
          enabled: _isEditing,
          decoration: InputDecoration(
            labelText: entry.key,
            border: const OutlineInputBorder(),
          ),
          validator: (value) {
            if (entry.key == 'SSN' || entry.key == 'First Name' || entry.key == 'Last Name') {
              if (value == null || value.isEmpty) {
                return 'Please enter a value for ${entry.key}';
              }
            }
            return null;
          },
        ),
      );
    }).toList();
  }
}

// Main function to run the app for testing
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    final customerService = CustomerService();

    return MaterialApp(
      title: 'Customer Details Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        brightness: Brightness.dark,
      ),
      home: FutureBuilder<Customer>(
        future: customerService.getCustomer(1),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Scaffold(
              body: Center(child: CircularProgressIndicator()),
            );
          } else if (snapshot.hasError) {
            return Scaffold(
              body: Center(child: Text("Error: ${snapshot.error}")),
            );
          } else if (snapshot.hasData) {
            return CustomerDetailsScreen(
              customer: snapshot.data!,
              customerService: customerService,
            );
          } else {
            return const Scaffold(
              body: Center(child: Text("No customer data found.")),
            );
          }
        },
      ),
    );
  }
}
