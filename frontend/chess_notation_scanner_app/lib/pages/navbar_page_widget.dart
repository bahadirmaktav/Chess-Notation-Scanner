import 'package:chess_notation_scanner_app/pages/home_page_widget.dart';
import 'package:chess_notation_scanner_app/pages/profile_page_widget.dart';
import 'package:chess_notation_scanner_app/pages/scan_page_widget.dart';
import 'package:flutter/material.dart';

class NavbarPageWidget extends StatefulWidget {
  const NavbarPageWidget({super.key});

  @override
  State<NavbarPageWidget> createState() => _NavbarPageWidgetState();
}

class _NavbarPageWidgetState extends State<NavbarPageWidget> {
  int _selectedIndex = 0;
  final List<Widget> _pages = [
    const ProfilePageWidget(),
    const HomePageWidget(),
    const ScanPageWidget()
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Profile',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.qr_code_scanner),
            label: 'Scan',
          ),
        ],
      ),
    );
  }
}
