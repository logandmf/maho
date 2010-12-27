#!/usr/bin/python

import sys, string, irclib, sqlite3, re

irclib.DEBUG = True

host = "irc.irchighway.net"
port = 6667
nick = "Maho"
channel = "#AINO"
database = "/usr/share/maho/maho"

def add_frase(table, col):
	sql = sqlite3.connect(database)
	q = sql.cursor()
	q.execute("INSERT INTO %s VALUES ('%s')" % (table, col.strip()))
	sql.commit()
	q.close()
	sql.close()
	return 'Adicionado com sucesso! ^^'

def query(table):
	sql = sqlite3.connect(database)
	q = sql.cursor()
	q.execute("SELECT sentence FROM '%s' ORDER BY RANDOM() LIMIT 1;" % table)
	phrase = q.fetchone()[0].encode('utf8')
	q.close()
	sql.close()
	return phrase

def query_all(table):
	sql = sqlite3.connect(database)
	q = sql.cursor()
	q.execute("SELECT sentence FROM '%s';" % table)
	phrase = q.fetchall()
	q.close()
	sql.close()
	return phrase

def handlePubMessage( connection, event ):
	for riso in query_all('risos'):
		riso = ' '.join( riso )
		if event.arguments()[0].decode('latin1').lower().find( riso ) == 0:
			phrase = query( 'piadas' )
			connection.privmsg( event.target(), event.source().split('!')[0] + ': %s' % phrase )

	if event.source().split('!')[0].lower().find( 'nataliagood' ) == 0 and event.arguments()[0].split(':')[0].find( nick ) == 0:
		phrase = query( 'natalia' )
		connection.privmsg( event.target(), event.source().split('!')[0] + ': %s' % phrase )
		connection.action( event.target(), '~~rolleyes~~')
	elif event.arguments()[0].split(':')[0].find( nick ) == 0 or event.arguments()[0].find( '[' + nick + ']' ) == 0 or event.arguments()[0].find( '(' + nick + ')' ) == 0:
		phrase = query( 'phrases' )
		connection.privmsg( event.target(), event.source().split('!')[0] + ': %s' % phrase )

	if event.arguments()[0].split(':')[0].find( '!add_frase_naty' ) == 0 and event.source().split('!')[0].lower().find( 'nataliagood' ) == 0:
		result = add_frase( 'natalia', event.arguments()[0].split(':')[1] )
		connection.action( event.target(), '%s' % result )
	elif event.arguments()[0].split(':')[0].find( '!add_frase' ) == 0:
		result = add_frase( 'phrases', event.arguments()[0].split(':')[1] )
		connection.action( event.target(), '%s' % result )

	if event.arguments()[0].split(':')[0].find( '!add_quote' ) == 0:
		result = add_frase( 'quotes', event.arguments()[0].split(':')[1] )
		connection.action( event.target(), '%s' % result )

	if event.arguments()[0].find( '!quote' ) == 0:
		phrase = query( 'quotes' )
		connection.privmsg( event.target(), event.source().split('!')[0] + ': %s' % phrase )

	if event.arguments()[0].find( '!help' ) == 0:
		cmds = [ '!add_frase_naty:', '!add_frase:', '!help' ]
		connection.privmsg( event.target(), '%s  %s  %s' % (cmds[0], cmds[1], cmds[2]) )

def handleJoin( connection, event ):
	phrase = query( 'join' )
	if event.source().split('!')[0].find( nick ) != 0:
		connection.privmsg( event.target(), event.source().split('!')[0] + ': %s' % phrase )

def handleQuit( connection, event ):
	phrase = query( 'quit' )
	if event.source().split('!')[0].find( nick ) != 0:
		connection.privmsg( channel, event.source().split('!')[0] + ': %s' % phrase )

irc = irclib.IRC()

irc.add_global_handler( 'join', handleJoin )
irc.add_global_handler( 'quit', handleQuit )
irc.add_global_handler( 'pubmsg', handlePubMessage )

server = irc.server()
server.connect( host, port, nick, ircname = nick )
server.join( channel )

irc.process_forever()
