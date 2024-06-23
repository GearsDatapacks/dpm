package changelog

import (
	"bytes"
	"log"
	"os"
	"strings"

	"github.com/gearsdatapacks/dpm/types"
)

type parser struct {
	src []byte
	pos int
}

func ParseChangelog(file string, expectedVersion types.Version) string {
	contents, err := os.ReadFile(file)
	if err != nil {
		log.Fatal(err)
	}

	p := parser{
		src: contents,
		pos: 0,
	}

	return p.parse(expectedVersion)
}

func (p *parser) parse(expectedVersion types.Version) string {
	for {
		ok := p.findHeader()
		if !ok {
			return ""
		}

		startPos := p.pos
		p.pos += 2
		p.skipWhitespace()

		version := p.parseVersion()
		if version == nil {
			continue
		}
		if *version == expectedVersion {
			p.findHeader()
			return strings.TrimSpace(string(p.src[startPos:p.pos]))
		}
	}
}

func (p *parser) findHeader() bool {
	headingLevel := 0
	for p.pos < len(p.src)-1 {
		if p.next() == '#' {
			headingLevel++
		} else if headingLevel == 2 {
			p.pos -= 2
			return true
		} else {
			headingLevel = 0
		}
		
		p.consume()
	}
	return false
}

func (p *parser) parseVersion() *types.Version {
	hasBrackets := p.next() == '['
	if hasBrackets {
		p.consume()
	}

	var versionStr bytes.Buffer
	for !(hasBrackets && p.next() == ']') && !isWhitespace(p.next()) {
		versionStr.WriteByte(p.consume())
	}

	version, err := types.ParseVersion(versionStr.String())
	if err != nil {
		return nil
	}
	return version
}

func (p *parser) next() byte {
	return p.peek(0)
}

func (p *parser) peek(offset int) byte {
	return p.src[p.pos+offset]
}

func (p *parser) consume() byte {
	next := p.next()
	p.pos++
	return next
}

func (p *parser) skipWhitespace() {
	for isWhitespace(p.next()) {
		p.consume()
	}
}

func isWhitespace(c byte) bool {
	return c == '\n' || c == '\r' || c == '\t' || c == ' '
}
