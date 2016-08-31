#!/usr/bin/env python
# coding=utf-8

def streamRef(stream, n):
    while n > 0:
        value = stream.next()
        n -= 1
    return value

def streamMap(proc, *streams):
    while True:
        args = map(lambda stream : stream.next(), streams)
        yield proc(*args)

def streamFilter(pred, stream):
    while True:
        value = stream.next()
        if pred(value):
            yield value

def scaleStream(stream, factor):
    while True:
        yield stream.next() * factor

def addStreams(stream1, stream2):
    return streamMap(int.__add__, stream1, stream2)

def partialSums(stream):
    sum = stream.next()
    yield sum 
    while True:
        sum += stream.next()
        yield sum

def integersStartingFrom(n):
    while True:
        yield n
        n += 1
    
def sieve(stream):
    while True:
        value = stream.next()
        yield value
        stream = streamFilter(lambda x: x % value != 0, stream)
primes = sieve(integersStartingFrom(2))


def piSummands(n):
    sign = 1
    yield 1.0 / n 
    while True:
        n += 2
        sign *= -1
        yield sign * 1.0 / n

piStream =  scaleStream(partialSums(piSummands(1)), 4) 

def lnSummands(n):
    sign = 1
    yield 1.0 / n
    while True:
        n += 1
        sign *= -1
        yield sign * 1.0 / n

lnStreams = partialSums(lnSummands(1))

def eulerTransform(stream):
    value1 = stream.next()
    value2 = stream.next()
    while True:
        value3 = stream.next()
        denom = value1 - 2 * value2 + value3
        if denom == 0:
            raise StopIteration
        else:
            yield value3 - (value3 - value2) ** 2 / (value1 - 2 * value2 + value3)
            value1, value2 = value2, value3

def makeTableau(transform, stream):
    yield stream
    while True:
        stream = transform(stream)
        yield stream

def accleratedSequence(transform, stream):
    return streamMap(lambda stream: stream.next(), makeTableau(transform, stream))
